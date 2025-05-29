import shutil

src = "/var/lib/tor/hidden_service"
dst = "/var/lib/tor/hidden_service_backup"
shutil.copytree(src, dst, dirs_exist_ok=True)
print(f"Clés copiées de {src} vers {dst}")
