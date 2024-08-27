#!/bin/bash

mkdir temp && cd temp
wget -O 1.tar.gz "https://gitlab.com/Dimbreath/AnimeGameData/-/archive/master/AnimeGameData-master.tar.gz?path=BinOutput/Talent/AvatarTalents"
tar xvzf 1.tar.gz
mv AnimeGameData-master-BinOutput-Talent-AvatarTalents/BinOutput/Talent/AvatarTalents/* ./
rm -rf 1.tar.gz AnimeGameData-master-BinOutput-Talent-AvatarTalents
cd ..
