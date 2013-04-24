import os
from fabric.api import run

WEBAPP_DIR = "/storage/www/tripvi/web"

def ruby_version():
  run("ruby --version")

def ignore_code_changes():
  cmds = []
  cmds.append("cd %s" % (WEBAPP_DIR, ))
  cmds.append("git reset --hard")

  run(" && ".join(cmds))


def update_code(exec_bundle=True):
  cmds = []
  cmds.append("cd %s" % (WEBAPP_DIR, ))
  cmds.append("git pull origin")
  if exec_bundle:
    cmds.append("bundle")

  run(" && ".join(cmds))


def precompile_assets(clean=True):
  cmds = []
  cmds.append("cd %s" % (WEBAPP_DIR, ))
  if clean:
    cmds.append("rake assets:clean")
  cmds.append("rake assets:precompile")

  run(" && ".join(cmds))


def restart_background_process():
  cmds = []
  cmds.append("cd %s" % (WEBAPP_DIR, ))
  cmds.append("RAILS_ENV=production script/delayed_job stop")
  cmds.append("RAILS_ENV=production script/delayed_job -m start")

  run(" && ".join(cmds))


def reload_unicorn():
  cmds = []
  cmds.append("cd %s" % (WEBAPP_DIR, ))
  cmds.append("script/init.unicorn.rb reload")

  run(" && ".join(cmds))


def deploy(assets_task=True, background_task=True):
  cmds = []
  cmds.append( update_code )

  if assets_task:
    cmds.append( precompile_assets )

  if background_task:
    cmds.append( restart_background_process )

  cmds.append( reload_unicorn )

  for cmd in cmds:
    cmd()


