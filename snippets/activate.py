import os
import shutil
source ='./test_fonts/Roboto-Black.ttf'

# FIXME: Use proper path manipulators
# Get the /home/<usr_name>/.fonts
from sugar3 import env
temp = env.get_profile_path()
temp = temp.split('/')
temp = temp[1:3]
temp = "/%s/%s" % (temp[0], temp[1])
dest = os.path.join(temp, '.fonts', 'Roboto-Black.ttf')

# Copy file to the destination
shutil.copyfile(source, dest)

# FIXME: Make this more efficient, and validate the output
import subprocess

bash_cmd = "fc-cache -f"
p = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
output, err = p.communicate()
print  output
