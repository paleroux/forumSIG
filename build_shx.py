#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
    (re)Construit le fichier index .shx correspondant au fichier .shp

    remarques :

    - seuls des modules standards Python sont utilisés (les fichiers .shp et
      .shx sont traités comme de simples fichiers)

    - la présence d'objet "vide" (null shape) N'a PAS été prévue (encore moins testée)

    - les shapefiles de type MultiPatch n'ont pas été pris en compte

    - écrit et testé en version 2.7, sous linux (Xubuntu) et MacOSX

    - outil "coin de table" et proposé à des fins pédagogiques : aucune gestion
      des exceptions

"""

from struct import pack, unpack, unpack_from

HEADER_SIZE = 100
FILE_LENGTH_OFFSET  = 24

# ATTENTION !!! les tailles et offsets se comptent en "mots" de 16 bits !!!
# ("ESRI Shapefile Technical Description", Juillet 1998, Tables 1 et 2, pages 4 et 5)

def build_shx(shp_pathname):

    # construction du chemin pour le .shx
    shx_pathname = os.path.splitext(shp_pathname)[0] + '.shx'

    # ouverture dans les bons modes
    shp = open(shp_pathname, 'rb')
    shx = open(shx_pathname, 'wb+')

    # lecture du header, récupération de la (demie-)taille du .shp
    header = shp.read(HEADER_SIZE)
    shp_size = 2 * unpack_from('>I', header, FILE_LENGTH_OFFSET)[0]

    # même header (à la (demie-)taille près)
    shx.write(header)

    # parcours des objets shape
    offset = HEADER_SIZE
    while offset < shp_size:

        # lecture du header du record
        _, recsize = unpack('>2I', shp.read(8))

        # écriture de l'offset et de la taille dans .shx
        shx.write(pack('>2I', offset/2, recsize))

        # positionnement sur l'objet suivant dans .shp, màj offset courant
        shp.seek(recsize*2, 1)
        offset = shp.tell()

    # mise à jour de la (demie-)taille dans le header
    shx_size = shx.tell()
    shx.seek(FILE_LENGTH_OFFSET)
    shx.write(pack('>I', shx_size/2))

    shx.close()
    shp.close()

if __name__ == '__main__':
    import sys
    build_shx(sys.argv[1])

