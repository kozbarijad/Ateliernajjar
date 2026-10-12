# Atelier Najjar — fichiers de marque

## Le logo

نجّار (Najjar en arabe) associé à « ATELIER NAJJAR » en capitales légèrement espacées.

| Dossier | Contenu | Pour quoi faire |
|---|---|---|
| `svg/` | Logos vectoriels (texte converti en tracés) | Imprimeur, graphiste, signalétique, gravure : qualité infinie, s'ouvrent sans les polices |
| `png/` | Les mêmes logos en PNG à fond transparent, 2400 px | Word, PowerPoint, Canva, signature d'email, devis |
| `favicon/` | Monogramme N en 16 à 512 px, `.ico` et `.svg` | Icône du site, onglet du navigateur |
| `reseaux/` | Photos de profil 1080 × 1080 px | Instagram, LinkedIn, WhatsApp Business |

### Quelle version utiliser

- **logo-vertical** : version principale (نجّار au-dessus du nom). Emballages, cartes de visite, devis, première page d'un document.
- **logo-vertical-bordeaux-baseline** : avec « Cuisine libanaise · Paris ». Supports de présentation, flyers.
- **logo-horizontal** : version en ligne. Menu du site, en-tête de document, signature d'email.
- **monogramme-N** : quand la place manque (favicon, tampon, autocollant rond).
- **monogramme-N-noun** (N + ن) : photo de profil sur les réseaux.

### Couleurs du logo

- **bordeaux** : sur fond clair (ivoire, blanc, kraft). C'est la version par défaut.
- **brun** : impression une couleur, documents sobres.
- **ivoire** : sur fond bordeaux ou foncé.
- **ivoire-or** : sur fond bordeaux, avec نجّار en or clair (pied de page du site).

Laisser autour du logo un espace libre au moins égal à la hauteur des lettres du nom. Ne pas déformer, recolorer ni ajouter d'ombre.

## Couleurs

| Nom | Hexadécimal | RVB | Usage |
|---|---|---|---|
| Bordeaux | `#5A1424` | 90, 20, 36 | Couleur de marque : logo, accents, bouton |
| Ivoire | `#FBF8F3` | 251, 248, 243 | Fond principal |
| Sable | `#ECE3D6` | 236, 227, 214 | Fond secondaire, fond des photos |
| Brun encre | `#2A1E1A` | 42, 30, 26 | Texte |
| Or | `#A88A5C` | 168, 138, 92 | Filets fins |
| Or clair | `#D9C29C` | 217, 194, 156 | Arabe du logo sur fond bordeaux |

Pour l'impression, faire convertir ces couleurs en CMJN ou Pantone par l'imprimeur à partir des valeurs ci-dessus.

## Polices

| Police | Usage | Licence |
|---|---|---|
| Tenor Sans | Nom « ATELIER NAJJAR » du logo | Libre (SIL OFL), Google Fonts |
| Amiri Bold | نجّار du logo | Libre (SIL OFL), Google Fonts |
| Libre Caslon Display | Titres du site et des documents | Libre (SIL OFL), Google Fonts |
| Helvetica Neue (ou Arial) | Texte courant | Installée sur Mac et PC |

Toutes ces polices se téléchargent gratuitement sur fonts.google.com, sauf Helvetica, déjà installée sur Mac.

## Modifier le logo

Les fichiers sont générés par `outils/marque.py` (Python, avec `fonttools` et `uharfbuzz`).
