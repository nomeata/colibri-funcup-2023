with import <nixpkgs> {};

stdenv.mkDerivation rec {
  name = "env";
  buildInputs = [
    gdal
    gpsbabel
    python3
    python3Packages.ipython
    python3Packages.pandas
    python3Packages.folium
#    python3Packages.shapely
#    python3Packages.geopy
    python3Packages.geographiclib
    python3Packages.snakeviz
    python3Packages.jinja2

    ( python3Packages.buildPythonPackage rec {
      pname = "pyopenair";
      version = "1.1.0"; # 1.2.0 needs shapely-2
      propagatedBuildInputs = [ python3Packages.shapely ];
      src = python3Packages.fetchPypi {
        inherit pname version;
        sha256 = "sha256-/ZmtxuBymqvb6oraFGMV6/4c2xhBs6ZFiqJPAzVoYEI=";
      };
      doCheck = false;
    })


  ];
}
