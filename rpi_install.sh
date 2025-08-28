sudo apt update
sudo apt install mpv libmpv2 libmpv-dev

arch=$(dpkg-architecture -qDEB_HOST_MULTIARCH)
mkdir -p ~/.local/lib
ln -s /usr/lib/$arch/libmpv.so.2 ~/.local/lib/libmpv.so.1