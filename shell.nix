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
  ];
}
