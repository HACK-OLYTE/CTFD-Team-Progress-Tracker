# CTFD-Team-Progress-Tracker

**CTFD-Team-Progress-Tracker** est un plugin pour [CTFd](https://ctfd.io) permettant aux administrateurs de visualiser en détail la progression de chaque équipe durant le CTF avec gestion intelligente des prérequis.

---

## Fonctionnalités principales

- **Visualisation complète de la progression** :
  - Affichage détaillé du statut de chaque challenge pour une équipe sélectionnée.
  - Interface moderne et intuitive avec code couleur clair.
  - Vue par catégorie avec statistiques en temps réel.

- **Gestion intelligente des prérequis** :
  - Détecte automatiquement les challenges bloqués par des prérequis non résolus.
  - Affiche clairement les dépendances entre challenges.
  - Calcule la progression réelle en tenant compte de l'accessibilité des challenges.

- **4 statuts de challenges distincts** :
  - ✅ **Résolu** : Challenge complété avec date et heure de résolution
  - ⚠️ **Tenté** : Challenge accessible mais non résolu (avec nombre de tentatives)
  - 🔒 **Bloqué** : Challenge non accessible car les prérequis ne sont pas remplis
  - 👁️ **Accessible** : Challenge débloqué mais pas encore tenté

- **Statistiques détaillées** :
  - Progression globale de l'équipe (pourcentage)
  - Statistiques par catégorie avec barres de progression animées
  - Compteur de tentatives par challenge
  - Vue chronologique des résolutions

- **Interface responsive et moderne** :
  - Design avec effets glassmorphism et animations fluides
  - Système de grille adaptatif (s'ajuste au nombre de challenges)
  - Cartes colorées par statut avec effets de survol
  - Compatible mobile et desktop

## Pourquoi ce plugin ?

> "Comment suivre efficacement la progression d'une équipe et identifier les blocages ?"

Avec ce plugin, les organisateurs peuvent :
- **Comprendre les difficultés** : Identifier rapidement quels challenges posent problème
- **Analyser la progression** : Voir si une équipe est bloquée par des prérequis
- **Optimiser le CTF** : Détecter les challenges trop difficiles ou mal placés dans l'arbre de dépendances
- **Assister les équipes** : Intervenir de manière ciblée pour débloquer une équipe
- **Analyser les performances** : Comparer les progressions et identifier les patterns

Les administrateurs gagnent une vision claire et détaillée de l'avancement de chaque équipe, permettant un suivi optimal du CTF et une meilleure expérience pour les participants.

## Installation

1. Clonez ce dépôt dans le dossier `CTFd/plugins` :
```bash
   cd /path/to/CTFd/plugins
   git clone https://github.com/HACK-OLYTE/CTFD-Team-Progress-Tracker.git
```

2. Redémarrez votre instance CTFd pour charger le plugin.

## Utilisation

### Accès au plugin

1. Connectez-vous en tant qu'administrateur
2. Allez dans **Admin Panel > Plugins > Team Progress Tracker**
3. Sélectionnez une équipe dans le menu déroulant
4. La progression détaillée s'affiche automatiquement

### Interface

**En-tête** : 
- Sélection d'équipe
- Légende des statuts

**Statistiques globales** :
- Nombre total de challenges résolus
- Pourcentage de progression
- Répartition par statut (Tentés / Bloqués / Accessibles)

**Vue par catégorie** :
- Chaque catégorie affiche ses statistiques propres
- Barre de progression visuelle
- Grille de cartes pour chaque challenge

**Cartes de challenges** :
- Nom du challenge
- Points
- Statut actuel
- Nombre de tentatives
- Date de résolution (si résolu)
- Prérequis (avec indication si bloqué ou débloqué)
  
## Fonctionnement technique

Le plugin :
1. Récupère tous les challenges visibles du CTF
2. Parse les prérequis (prerequisites) définis dans chaque challenge
3. Récupère les solves de l'équipe sélectionnée
4. Calcule quels challenges sont accessibles selon les dépendances
5. Compte les tentatives (submissions) par challenge
6. Détermine le statut de chaque challenge :
   - **Solved** : Challenge dans les solves de l'équipe
   - **Locked** : Prérequis non remplis
   - **Attempted** : Accessible + au moins 1 tentative
   - **Accessible** : Accessible + 0 tentative
7. Affiche le tout dans une interface interactive

## Dépendances

- CTFd ≥ v3.8.1
- Compatible avec les installations Docker et locales
- Un navigateur à jour avec JavaScript activé
- CTFd thème : Core-beta (testé et optimisé)
- Mode équipe ou mode utilisateur de CTFd

## Sécurité

Ce plugin a été conçu avec la sécurité en priorité :
- ✅ Protection XSS complète (`.textContent` + DOM manipulation)
- ✅ Routes admin protégées avec `@admins_only`
- ✅ Pas d'injection SQL (utilisation ORM SQLAlchemy)
- ✅ Validation des team_id (vérification d'existence)
- ✅ Filtrage des équipes bannies
- ✅ Error handling robuste avec logging
- ✅ Validation stricte des prérequis (entiers uniquement)

## Démonstration du fonctionnement du plugin



## Cas d'usage

### 1. Support aux équipes
Identifiez rapidement si une équipe est bloquée et intervenez de manière ciblée.

### 2. Analyse de difficulté
Détectez les challenges qui posent problème à la majorité des équipes.

### 3. Optimisation de l'arbre de dépendances
Vérifiez que les prérequis sont bien configurés et que la progression est fluide.

### 4. Statistiques post-CTF
Analysez les patterns de résolution pour améliorer vos futurs événements.

### 5. Validation de la configuration
Vérifiez que tous les challenges sont accessibles via le bon chemin de prérequis.

## Démonstration du plugin 


https://github.com/user-attachments/assets/fd262fdd-6c8f-456b-8149-10d2b98d810d




## Limitations

- Affichage limité à une équipe à la fois (pas de vue comparative)
- Nécessite que les prérequis soient correctement configurés dans CTFd
- Calcul en temps réel à chaque chargement (pas de cache)
- Compatible uniquement avec le système de prérequis natif de CTFd

## Compatibilité

✅ CTFd v3.x  
✅ Mode Team  
✅ Mode User  
✅ Docker  
✅ Installation locale  
✅ Prérequis natifs CTFd  

## Support

Pour toute question ou problème, ouvrez une [issue](https://github.com/HACK-OLYTE/CTFD-Team-Progress-Tracker/issues).  
Ou contactez-nous sur le site de l'association Hack'olyte : [contact](https://hackolyte.fr/contact/).

## Contribuer

Les contributions sont les bienvenues !  
Vous pouvez :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests
- Améliorer la documentation
- Partager vos suggestions d'amélioration

## Crédits

Développé avec ❤️ par l'association [Hack'olyte](https://hackolyte.fr)

## Licence

Ce plugin est sous licence [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/deed.fr).  
Merci de ne pas retirer les crédits sans l'autorisation préalable de l'association Hack'olyte.

---

**Note** : Ce plugin fonctionne en lecture seule et n'affecte en aucun cas les données du CTF. Il est conçu exclusivement pour l'administration et le suivi des équipes.


