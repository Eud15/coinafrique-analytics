"""
Module de nettoyage des données Web Scraper
Auteur: Eudoxie - DIT Master AI
Date: Janvier 2026
"""

import pandas as pd
import re
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)

class NettoyeurDonnees:
    """Nettoie les données brutes issues de Web Scraper (extension Chrome)"""
    
    def __init__(self):
        self.stats_nettoyage = {
            'lignes_initiales': 0,
            'lignes_finales': 0,
            'doublons_supprimes': 0,
            'lignes_invalides': 0
        }
    
    @staticmethod
    def nettoyer_prix(prix) -> str:
        """Nettoie et standardise le prix"""
        if pd.isna(prix) or not prix or prix == '':
            return "Prix sur demande"
        
        prix_str = str(prix).strip()
        
        # Vérifier si c'est "Prix sur demande"
        if any(x in prix_str.lower() for x in ['demande', 'négociable', 'appeler']):
            return "Prix sur demande"
        
        # Extraire les chiffres
        nombres = re.findall(r'\d+[\s\d]*', prix_str)
        if nombres:
            # Nettoyer et formater
            prix_nettoye = nombres[0].replace(' ', '').replace('\xa0', '').replace('.', '')
            try:
                prix_int = int(prix_nettoye)
                return f"{prix_int} CFA"
            except:
                pass
        
        return "Prix non disponible"
    
    @staticmethod
    def nettoyer_texte(texte) -> str:
        """Nettoie les espaces et caractères superflus"""
        if pd.isna(texte) or not texte:
            return ""
        
        texte_str = str(texte)
        # Supprimer les espaces multiples, tabs, retours à la ligne
        texte_clean = ' '.join(texte_str.split())
        # Supprimer les caractères spéciaux problématiques
        texte_clean = texte_clean.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        return texte_clean.strip()
    
    @staticmethod
    def nettoyer_adresse(adresse) -> str:
        """Nettoie et standardise l'adresse"""
        if pd.isna(adresse) or not adresse:
            return "Adresse non disponible"
        
        adresse_str = str(adresse).strip()
        
        # Nettoyer les espaces
        adresse_clean = ' '.join(adresse_str.split())
        
        # Standardiser "Sénégal"
        adresse_clean = re.sub(
            r'S[ée]n[ée]gal',
            'Sénégal',
            adresse_clean,
            flags=re.IGNORECASE
        )
        
        # Capitaliser correctement
        if ',' in adresse_clean:
            parties = [p.strip().capitalize() for p in adresse_clean.split(',')]
            adresse_clean = ', '.join(parties)
        
        return adresse_clean if adresse_clean else "Adresse non disponible"
    
    @staticmethod
    def nettoyer_image_lien(lien) -> str:
        """Nettoie et valide le lien image"""
        if pd.isna(lien) or not lien:
            return ""
        
        lien_str = str(lien).strip()
        
        # Vérifier si c'est une URL valide
        if lien_str.startswith('http://') or lien_str.startswith('https://'):
            return lien_str
        elif lien_str.startswith('//'):
            return f"https:{lien_str}"
        elif lien_str.startswith('/'):
            return f"https://sn.coinafrique.com{lien_str}"
        
        return lien_str if lien_str else ""
    
    def detecter_colonnes(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Détecte automatiquement les colonnes dans le DataFrame brut
        
        Returns:
            Dictionnaire {type_standard: nom_colonne_dans_df}
        """
        mapping = {
            'type': None,
            'prix': None,
            'adresse': None,
            'image': None
        }
        
        colonnes_lower = {col.lower(): col for col in df.columns}
        
        # Détection du type/titre
        for pattern in ['type', 'titre', 'nom', 'produit', 'title', 'name', 'item']:
            for col_lower, col_original in colonnes_lower.items():
                if pattern in col_lower and not mapping['type']:
                    mapping['type'] = col_original
                    break
        
        # Détection du prix
        for pattern in ['prix', 'price', 'montant', 'amount', 'cost']:
            for col_lower, col_original in colonnes_lower.items():
                if pattern in col_lower and not mapping['prix']:
                    mapping['prix'] = col_original
                    break
        
        # Détection de l'adresse
        for pattern in ['adresse', 'localisation', 'location', 'ville', 'city', 'lieu', 'address']:
            for col_lower, col_original in colonnes_lower.items():
                if pattern in col_lower and not mapping['adresse']:
                    mapping['adresse'] = col_original
                    break
        
        # Détection de l'image
        for pattern in ['image', 'img', 'photo', 'picture', 'pic']:
            for col_lower, col_original in colonnes_lower.items():
                if pattern in col_lower and not mapping['image']:
                    mapping['image'] = col_original
                    break
        
        return mapping
    
    def nettoyer_dataframe(
        self,
        df: pd.DataFrame,
        categorie: str,
        mapping_colonnes: Dict[str, str] = None
    ) -> pd.DataFrame:
        """
        Nettoie un DataFrame complet issu de Web Scraper
        
        Args:
            df: DataFrame brut
            categorie: 'vetements' ou 'chaussures'
            mapping_colonnes: Mapping manuel des colonnes (optionnel)
            
        Returns:
            DataFrame nettoyé
        """
        logging.info(f"🧹 Début du nettoyage pour catégorie: {categorie}")
        
        self.stats_nettoyage['lignes_initiales'] = len(df)
        df_clean = df.copy()
        
        # Détection automatique des colonnes si pas de mapping fourni
        if not mapping_colonnes:
            mapping_colonnes = self.detecter_colonnes(df_clean)
            logging.info(f"📋 Colonnes détectées: {mapping_colonnes}")
        
        # Créer le nouveau DataFrame avec colonnes standardisées
        df_result = pd.DataFrame()
        
        # Type de produit
        col_type = 'type_habits' if categorie == 'vetements' else 'type_chaussures'
        if mapping_colonnes['type']:
            df_result[col_type] = df_clean[mapping_colonnes['type']].apply(self.nettoyer_texte)
        else:
            df_result[col_type] = "Non disponible"
        
        # Prix
        if mapping_colonnes['prix']:
            df_result['prix'] = df_clean[mapping_colonnes['prix']].apply(self.nettoyer_prix)
        else:
            df_result['prix'] = "Prix non disponible"
        
        # Adresse
        if mapping_colonnes['adresse']:
            df_result['adresse'] = df_clean[mapping_colonnes['adresse']].apply(self.nettoyer_adresse)
        else:
            df_result['adresse'] = "Adresse non disponible"
        
        # Image
        if mapping_colonnes['image']:
            df_result['image_lien'] = df_clean[mapping_colonnes['image']].apply(self.nettoyer_image_lien)
        else:
            df_result['image_lien'] = ""
        
        # Supprimer les doublons
        avant_doublons = len(df_result)
        df_result = df_result.drop_duplicates()
        self.stats_nettoyage['doublons_supprimes'] = avant_doublons - len(df_result)
        
        # Supprimer les lignes sans information utile
        avant_invalides = len(df_result)
        df_result = df_result[
            (df_result[col_type].str.len() > 3) &
            (df_result[col_type] != "Non disponible")
        ]
        self.stats_nettoyage['lignes_invalides'] = avant_invalides - len(df_result)
        
        # Reset index
        df_result = df_result.reset_index(drop=True)
        
        self.stats_nettoyage['lignes_finales'] = len(df_result)
        
        logging.info(f"✅ Nettoyage terminé:")
        logging.info(f"   • Lignes initiales: {self.stats_nettoyage['lignes_initiales']}")
        logging.info(f"   • Doublons supprimés: {self.stats_nettoyage['doublons_supprimes']}")
        logging.info(f"   • Lignes invalides: {self.stats_nettoyage['lignes_invalides']}")
        logging.info(f"   • Lignes finales: {self.stats_nettoyage['lignes_finales']}")
        
        return df_result
    
    def get_stats(self) -> Dict:
        """Retourne les statistiques du dernier nettoyage"""
        return self.stats_nettoyage.copy()


def test_nettoyage():
    """Fonction de test du module"""
    print("\n" + "="*70)
    print("🧪 TEST DU MODULE DE NETTOYAGE")
    print("="*70 + "\n")
    
    # Créer des données de test
    data_test = {
        'Titre': ['T-shirt Nike', 'Jean Levis  ', 'Basket Adidas', 'T-shirt Nike'],
        'Prix': ['15000 CFA', '  25 000 F CFA', 'Prix sur demande', '15000 CFA'],
        'Localisation': ['Dakar, senegal', 'Thiès,  Sénégal', 'Rufisque, Sénégal', 'Dakar, senegal'],
        'Image': ['/img/1.jpg', 'https://example.com/2.jpg', '//cdn.example.com/3.jpg', '/img/1.jpg']
    }
    
    df_test = pd.DataFrame(data_test)
    
    print("📊 Données brutes:")
    print(df_test)
    print(f"\nNombre de lignes: {len(df_test)}")
    
    # Nettoyer
    nettoyeur = NettoyeurDonnees()
    df_clean = nettoyeur.nettoyer_dataframe(df_test, 'vetements')
    
    print("\n" + "-"*70)
    print("\n✨ Données nettoyées:")
    print(df_clean)
    
    print("\n" + "-"*70)
    print("\n📈 Statistiques:")
    stats = nettoyeur.get_stats()
    for cle, valeur in stats.items():
        print(f"   • {cle}: {valeur}")
    
    print("\n" + "="*70)
    print("✅ TEST TERMINÉ")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_nettoyage()