from re import sub
from subprocess import run
from configparser import ConfigParser
from glob import glob

job_conf = ConfigParser()
job_conf_ini = './job.conf'
shares_conf = './shares.conf'

def get_config():
	global job_conf
	job_conf.read(job_conf_ini)
	
def build_shares():
	shares = []
	with open(shares_conf,'r') as f:
		for line in f.readlines():
			src_dest = line.split(' ')
			job=(sub(r'[\n\t\s]*', '', src_dest[0]), sub(r'[\n\t\s]*', '', src_dest[1]))
			shares.append(job)
	return shares

def sync_share(src,dst):
	rsync_flags = job_conf.get('Default', 'rsync_flags')
	src_base = job_conf.get('Default', 'src_base')
	dst_base = job_conf.get('Default', 'dst_base')

	src_full = '%s/%s/*' % (src_base, src)
	dst_full = '%s/%s' % (dst_base, dst)

	print('\n### RUNNING JOB ###\n%s --> %s\n' %  (src_full, dst_full))

	files = glob(src_full)
	for file in files:
		print('running: rsync %s %s %s' % (rsync_flags, file, dst_full))
		run(['rsync', rsync_flags, file, dst_full], check=True, stdout=True)

def apply_share_permissions(dst):
	print('applying share permissions: %s' % dst)

def process_shares(shares):
	for share in shares:
		src = share[0]
		dst = share[1]
		sync_share(src, dst)
		apply_share_permissions(dst)

if __name__ == '__main__':
	get_config()
	shares = build_shares()
	process_shares(shares)