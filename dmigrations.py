#script for deleting migrations folder from django project.
# paste in project folder.
import os
import shutil
cwd= os.getcwd()
print("Deleting 'migrations' folder from '{0}'...".format(os.path.basename(cwd)))

for folder in os.listdir(cwd):
	if os.path.isdir(folder):
		parent_dir = os.path.join(cwd,folder)
		print("Deleting from '{0}'...".format(folder))
		for sub_folder in os.listdir(parent_dir):
			remove_dir = os.path.join(parent_dir,'migrations')
			shutil.rmtree(remove_dir,ignore_errors = True)
print("\n")
print("Deleted all 'migrations' folder from your project.\nNow Run:")
print("python manage.py makemigrations accounts batches courses dashboard exams fees institute notes results students teacher tutorials tutor")
