"""
Script de scraping CoinAfrique - Projet Master AI
Extraction des données avec BeautifulSoup
Auteur: Eudoxie - DIT Master AI
Date: Janvier 2026
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import List, Dict, Optional
import re
from urllib.parse import urljoin

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CoinAfriqueScraper:
    """Scraper pour extraire les données de CoinAfrique avec BeautifulSoup"""
    
    def __init__(self):
        self.base_url = "https://sn.coinafrique.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def extraire_nombre(self, texte: str) -> str:
        """Extrait le nombre d'une chaîne de caractères"""
        if not texte:
            return "Prix sur demande"
        
        texte = texte.strip()
        
        if "Prix sur demande" in texte or "sur demande" in texte.lower():
            return "Prix sur demande"
        
        nombres = re.findall(r'\d+[\s\d]*', texte)
        if nombres:
            prix_nettoye = nombres[0].replace(' ', '')
            return prix_nettoye + " CFA"
        
        return texte
    
    def nettoyer_texte(self, texte: str) -> str:
        """Nettoie un texte en enlevant les espaces superflus"""
        if not texte:
            return ""
        return ' '.join(texte.split())
    
    def scraper_une_page(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Scrape une seule page et retourne toutes les annonces
        
        Args:
            soup: Objet BeautifulSoup de la page
            
        Returns:
            Liste des annonces de cette page
        """
        annonces_page = []
        
        # Trouver toutes les annonces
        annonces_elements = soup.find_all('a', href=re.compile(r'/ad/|/annonce/'))
        
        if not annonces_elements:
            return annonces_page
        
        for element in annonces_elements:
            try:
                # Extraire le titre/type
                titre_elem = element.find('div') or element
                titre = self.nettoyer_texte(titre_elem.get_text()) if titre_elem else ""
                
                if not titre:
                    titre = element.get('title', '')
                
                # Extraire le prix
                prix = ""
                
                # Méthode 1: chercher dans les éléments frères précédents
                prix_elem = element.find_previous('div')
                tentatives = 0
                while prix_elem and tentatives < 5:
                    prix_text = prix_elem.get_text()
                    if 'CFA' in prix_text or 'F CFA' in prix_text or 'FCFA' in prix_text:
                        prix = self.extraire_nombre(prix_text)
                        break
                    prix_elem = prix_elem.find_previous('div')
                    tentatives += 1
                
                # Méthode 2: chercher dans les éléments enfants
                if not prix:
                    for child in element.find_all(['div', 'span', 'p']):
                        child_text = child.get_text()
                        if 'CFA' in child_text or 'F CFA' in child_text or 'FCFA' in child_text:
                            prix = self.extraire_nombre(child_text)
                            break
                
                # Méthode 3: chercher dans l'élément parent
                if not prix:
                    parent = element.parent
                    if parent:
                        for sibling in parent.find_all(['div', 'span', 'p']):
                            sibling_text = sibling.get_text()
                            if 'CFA' in sibling_text or 'F CFA' in sibling_text or 'FCFA' in sibling_text:
                                prix = self.extraire_nombre(sibling_text)
                                break
                
                if not prix:
                    prix = "Prix non disponible"
                
                # Extraire l'adresse
                adresse = ""
                
                # Méthode 1: chercher un élément contenant "Sénégal"
                location_elem = element.find_next('div', string=re.compile(r'.*[,].*[Ss][ée]n[ée]gal.*'))
                if not location_elem:
                    location_elem = element.find_next(string=re.compile(r'.*[,].*[Ss][ée]n[ée]gal.*'))
                
                if location_elem:
                    adresse = self.nettoyer_texte(
                        location_elem if isinstance(location_elem, str) else location_elem.get_text()
                    )
                
                # Méthode 2: chercher dans les éléments enfants
                if not adresse:
                    for child in element.find_all(['div', 'span', 'p']):
                        child_text = child.get_text()
                        if 'Sénégal' in child_text or 'senegal' in child_text.lower():
                            adresse = self.nettoyer_texte(child_text)
                            break
                
                # Méthode 3: chercher dans le parent
                if not adresse:
                    parent = element.parent
                    if parent:
                        for sibling in parent.find_all(['div', 'span', 'p']):
                            sibling_text = sibling.get_text()
                            if 'Sénégal' in sibling_text or 'senegal' in sibling_text.lower():
                                adresse = self.nettoyer_texte(sibling_text)
                                break
                
                # Méthode 4: chercher avec find_next_sibling
                if not adresse:
                    next_sibling = element.find_next_sibling()
                    if next_sibling:
                        sibling_text = next_sibling.get_text()
                        if 'Sénégal' in sibling_text or 'senegal' in sibling_text.lower():
                            adresse = self.nettoyer_texte(sibling_text)
                
                if not adresse:
                    adresse = "Adresse non disponible"
                
                # Extraire l'image
                image_elem = element.find('img')
                image_url = ""
                if image_elem:
                    image_url = image_elem.get('src', '') or image_elem.get('data-src', '') or image_elem.get('data-lazy-src', '')
                    if image_url and not image_url.startswith('http'):
                        image_url = urljoin(self.base_url, image_url)
                
                # Ajouter l'annonce si elle a des données valides
                if titre and len(titre) > 3:
                    annonce = {
                        'type': titre,
                        'prix': prix,
                        'adresse': adresse,
                        'image_lien': image_url
                    }
                    annonces_page.append(annonce)
                    
            except Exception as e:
                logging.debug(f"Erreur lors de l'extraction d'une annonce: {str(e)}")
                continue
        
        return annonces_page
    
    def scraper_page(self, url: str, max_pages: int = 5) -> List[Dict]:
        """
        Scrape plusieurs pages de CoinAfrique
        
        Args:
            url: URL de la catégorie à scraper
            max_pages: Nombre maximum de pages à scraper
            
        Returns:
            Liste de dictionnaires contenant les données des annonces
        """
        toutes_annonces = []
        page = 1
        
        logging.info(f"Début du scraping de: {url}")
        logging.info(f"Nombre de pages à scraper: {max_pages}")
        
        while page <= max_pages:
            try:
                # Construire l'URL de la page
                page_url = f"{url}?page={page}" if page > 1 else url
                
                logging.info(f"\n{'='*60}")
                logging.info(f"Scraping de la page {page}/{max_pages}")
                logging.info(f"URL: {page_url}")
                logging.info(f"{'='*60}")
                
                # Récupérer la page
                response = self.session.get(page_url, timeout=15)
                response.raise_for_status()
                
                # Parser le HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Scraper toutes les annonces de cette page
                annonces_page = self.scraper_une_page(soup)
                
                if not annonces_page:
                    logging.warning(f"Aucune annonce trouvée sur la page {page}")
                    logging.info("Arrêt du scraping (page vide)")
                    break
                
                # Ajouter les annonces de cette page au total
                toutes_annonces.extend(annonces_page)
                
                logging.info(f"✓ Page {page} terminée: {len(annonces_page)} annonces collectées")
                logging.info(f"  Total cumulé: {len(toutes_annonces)} annonces")
                
                # Pause entre les pages
                if page < max_pages:
                    logging.info("Pause de 2 secondes avant la page suivante...")
                    time.sleep(2)
                
                page += 1
                    
            except requests.exceptions.RequestException as e:
                logging.error(f"Erreur HTTP lors de la requête: {str(e)}")
                break
            except Exception as e:
                logging.error(f"Erreur inattendue: {str(e)}")
                break
        
        logging.info(f"\n{'='*60}")
        logging.info(f"SCRAPING TERMINÉ")
        logging.info(f"Pages scrapées: {page - 1}")
        logging.info(f"Total annonces: {len(toutes_annonces)}")
        logging.info(f"{'='*60}\n")
        
        return toutes_annonces
    
    def scraper_toutes_categories(self, max_pages_par_categorie: int = 5) -> Dict[str, pd.DataFrame]:
        """
        Scrape toutes les catégories définies dans le projet
        
        Args:
            max_pages_par_categorie: Nombre maximum de pages par catégorie
            
        Returns:
            Dictionnaire avec les DataFrames de chaque catégorie
        """
        # Définir les URLs des catégories
        categories = {
            'vetements_homme': {
                'url': 'https://sn.coinafrique.com/categorie/vetements-homme',
                'type_col': 'type_habits'
            },
            'chaussures_homme': {
                'url': 'https://sn.coinafrique.com/categorie/chaussures-homme',
                'type_col': 'type_chaussures'
            },
            'vetements_enfants': {
                'url': 'https://sn.coinafrique.com/categorie/vetements-enfants',
                'type_col': 'type_habits'
            },
            'chaussures_enfants': {
                'url': 'https://sn.coinafrique.com/categorie/chaussures-enfants',
                'type_col': 'type_chaussures'
            }
        }
        
        resultats = {}
        
        for nom_categorie, config in categories.items():
            logging.info(f"\n\n{'#'*70}")
            logging.info(f"# CATÉGORIE: {nom_categorie.upper().replace('_', ' ')}")
            logging.info(f"{'#'*70}\n")
            
            # Scraper la catégorie (par pages)
            annonces = self.scraper_page(config['url'], max_pages_par_categorie)
            
            # Convertir en DataFrame
            if annonces:
                df = pd.DataFrame(annonces)
                
                # Renommer la colonne 'type' selon la catégorie
                df.rename(columns={'type': config['type_col']}, inplace=True)
                
                # Réorganiser les colonnes dans l'ordre souhaité
                colonnes = [config['type_col'], 'prix', 'adresse', 'image_lien']
                df = df[colonnes]
                
                resultats[nom_categorie] = df
                
                # Sauvegarder dans un fichier CSV
                import os
                os.makedirs('data/nettoye', exist_ok=True)
                fichier_csv = f"data/nettoye/{nom_categorie}_nettoye.csv"
                df.to_csv(fichier_csv, index=False, encoding='utf-8-sig')
                
                logging.info(f"Fichier sauvegardé: {fichier_csv}")
                logging.info(f"Statistiques:")
                logging.info(f"  - Annonces totales: {len(df)}")
                logging.info(f"  - Colonnes: {', '.join(df.columns)}")
                
                # Statistiques sur les données manquantes
                prix_dispo = len(df[df['prix'] != 'Prix non disponible'])
                adresse_dispo = len(df[df['adresse'] != 'Adresse non disponible'])
                logging.info(f"  - Prix disponibles: {prix_dispo}/{len(df)} ({prix_dispo/len(df)*100:.1f}%)")
                logging.info(f"  - Adresses disponibles: {adresse_dispo}/{len(df)} ({adresse_dispo/len(df)*100:.1f}%)")
            else:
                logging.warning(f"Aucune donnée collectée pour {nom_categorie}")
        
        return resultats


def main():
    """Fonction principale pour tester le scraper"""
    print("\n" + "="*70)
    print("SCRAPER COINAFRIQUE - BEAUTIFULSOUP")
    print("Scraping par page")
    print("="*70 + "\n")
    
    scraper = CoinAfriqueScraper()
    
    # Scraper toutes les catégories (3 pages par catégorie)
    resultats = scraper.scraper_toutes_categories(max_pages_par_categorie=3)
    
    # Afficher un résumé
    print("\n" + "="*70)
    print("RÉSUMÉ DU SCRAPING")
    print("="*70 + "\n")
    
    for categorie, df in resultats.items():
        print(f"\n{categorie.upper().replace('_', ' ')}")
        print("-" * 50)
        print(f"  Nombre d'annonces: {len(df)}")
        print(f"  Colonnes: {', '.join(df.columns)}")
        
        # Statistiques
        prix_dispo = len(df[df['prix'] != 'Prix non disponible'])
        adresse_dispo = len(df[df['adresse'] != 'Adresse non disponible'])
        print(f"  Prix disponibles: {prix_dispo}/{len(df)} ({prix_dispo/len(df)*100:.1f}%)")
        print(f"  Adresses disponibles: {adresse_dispo}/{len(df)} ({adresse_dispo/len(df)*100:.1f}%)")
        
        print(f"\n  Aperçu des 3 premières lignes:")
        print(df.head(3).to_string(index=False))
        print()
    
    print("="*70)
    print("SCRAPING TERMINÉ AVEC SUCCÈS!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()