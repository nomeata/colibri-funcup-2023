{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    { devShell.${system} = pkgs.stdenv.mkDerivation rec {
      name = "env";
      buildInputs = with pkgs; [
        gdal
        gpsbabel
        python3
        python3Packages.ipython
        python3Packages.pandas
        python3Packages.folium
#       python3Packages.shapely
#       python3Packages.geopy
        python3Packages.geographiclib
        python3Packages.snakeviz
        python3Packages.jinja2
        python3Packages.numpy
        ( python3Packages.buildPythonPackage rec {
          pname = "pyopenair";
          version = "1.2.0"; # 1.2.0 needs shapely-2
          propagatedBuildInputs = [ python3Packages.shapely ];
          src = python3Packages.fetchPypi {
            inherit pname version;
            sha256 = "sha256-4GRTxuBx5G3GkKJjq8kysv+powan1MglKsBsIMYeg90=";
          };
          doCheck = false;
        })
      ];
   };};
}
