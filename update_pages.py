import os
import glob

html_files = glob.glob(r"c:\Users\sande\OneDrive\Desktop\E-Commerce\frontend\*.html")
exclude = ["index.html", "travel.html", "login.html"]

script_to_append = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const userJson = localStorage.getItem('lifoss_user');
            if (!userJson) {
                window.location.href = 'index.html';
                return;
            }
            const user = JSON.parse(userJson);
            const sidebarName = document.getElementById('sidebarNameDisplay');
            if(sidebarName) {
                sidebarName.innerText = user.name;
            }
        });
    </script>
</body>
</html>
"""

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in exclude:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Only process pages that haven't been fully customized yet (like profile.html)
    # Actually, we should just replace LIFOSS User with an empty span and an ID unconditionally
    
    # Replace hardcoded name with ID
    old_target = '<div style="font-weight: 600; font-size: 1.1rem;">LIFOSS User</div>'
    new_target = '<div style="font-weight: 600; font-size: 1.1rem;" id="sidebarNameDisplay"></div>'
    
    if old_target in content:
        content = content.replace(old_target, new_target)
    
    # If script isn't already in file, append it
    if "sidebarNameDisplay" in content and "localStorage.getItem('lifoss_user')" not in content:
        # replace the closing body tags
        content = content.replace("</body>\n</html>", script_to_append)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Patch applied globally!")
