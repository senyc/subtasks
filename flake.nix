{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in {
    # run nix develop
    devShells.x86_64-linux.default = pkgs.mkShell {
      packages = with pkgs; [
        (python3.withPackages (p:
          with p; [
            fastapi
            sqlmodel
            pytest
            alembic
          ]))
        fastapi-cli
        sqlite
      ];
    };
  };
}
