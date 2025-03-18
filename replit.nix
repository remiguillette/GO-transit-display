{pkgs}: {
  deps = [
    pkgs.playwright-driver
    pkgs.gitFull
    pkgs.geckodriver
    pkgs.curl
    pkgs.unzip
  ];
}
