{
  description = "yooxn (yooxnas) - Python tools for the Uxn ecosystem";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    ooze.url = "github:davidabram/ooze";
  };

  outputs =
    { self
    , nixpkgs
    , flake-utils
    , ooze
    }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        py = pkgs.python313;
        pyPkgs = pkgs.python313Packages;

        yooxn = pyPkgs.buildPythonApplication {
          pname = "yooxn";
          version = "1.0.0";
          pyproject = true;
          src = self;

          build-system = [
            pyPkgs.hatchling
          ];

          pythonImportsCheck = [
            "yooxn"
          ];
        };
      in
      {
        packages = {
          default = yooxn;
          yooxn = yooxn;
        };

        apps = {
          default = self.apps.${system}.yooxnas;
          yooxnas = {
            type = "app";
            program = "${yooxn}/bin/yooxnas";
          };
        };

        devShells.default = pkgs.mkShell {
          packages = [
            py
            pkgs.uv
            pyPkgs.pytest
            pyPkgs.ruff
            pyPkgs.mypy
            ooze.packages.${system}.default
          ];
        };
      });
}
