# Interdépendances entre modalités

## Types de liens

- **Contrainte** : Une modalité limite ou conditionne le fonctionnement d'une autre.
- **Instrument** : Une modalité fournit des outils ou des ressources à une autre.
- **Légitimation** : Une modalité justifie ou valide les opérations d'une autre.

## Liens principaux

| Source | Cible | Type | Description |
|--------|-------|------|-------------|
| Mythologie | Valeurs et Éthique | Légitimation | Les modèles du monde fondent les priorités éthiques |
| Valeurs et Éthique | Gouvernance | Légitimation | Les valeurs légitiment les règles de coordination |
| Gouvernance | Économie | Contrainte | Les règles encadrent l'allocation des ressources |
| Technique | Économie | Instrument | L'infrastructure supporte la production et les échanges |
| Culture | Mythologie | Instrument | Les pratiques partagées alimentent les modèles collectifs |
| Gouvernance | Culture | Contrainte | Les règles formatent les conventions d'exécution |

## Boucles structurantes

1. **Boucle de légitimation** : Mythologie → Valeurs → Gouvernance → Culture → Mythologie
2. **Boucle matérielle** : Technique → Économie → Gouvernance → Technique
3. **Boucle culturelle** : Culture → Valeurs → Culture

## Matrice d'interdépendances

Ordre : culture, mythologie, valeurs_ethique, gouvernance, economie, technique_infrastructure

```
         CUL   MYT   VAL   GOV   ECO   TEC
CUL     1.00  0.40  0.50  0.40  0.30  0.20
MYT     0.40  1.00  0.60  0.30  0.20  0.20
VAL     0.50  0.60  1.00  0.50  0.30  0.20
GOV     0.40  0.30  0.50  1.00  0.40  0.30
ECO     0.30  0.20  0.30  0.40  1.00  0.50
TEC     0.20  0.20  0.20  0.30  0.50  1.00
```

## Usage opérationnel

La matrice est utilisée pour calculer les influences croisées entre modalités lors de la mise à jour des indicateurs. Chaque coefficient représente la force du couplage entre deux modalités. La diagonale (1.0) représente l'auto-influence de chaque modalité. Les coefficients hors diagonale déterminent comment le score d'une modalité affecte les métriques des autres.
