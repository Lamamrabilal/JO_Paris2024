// JavaScript (script.js)
document.addEventListener('DOMContentLoaded', () => {
    // Sélectionner l'élément du compteur de panier
    const cartCountElement = document.querySelector('.cart-count');

    // Récupérer le nombre d'articles dans le panier depuis le stockage local du navigateur
    let nombreArticlesPanier = localStorage.getItem('nombreArticlesPanier');

    // Si le nombre d'articles dans le panier n'est pas déjà stocké, initialiser à zéro
    if (!nombreArticlesPanier) {
        nombreArticlesPanier = 0;
    } else {
        // Convertir en nombre car localStorage stocke tout en chaînes de caractères
        nombreArticlesPanier = parseInt(nombreArticlesPanier);
    }

    // Fonction pour mettre à jour le compteur du panier
    const mettreAJourCompteurPanier = (count) => {
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    };

    // Fonction pour ajouter un article au panier
    const ajouterAuPanier = () => {
        nombreArticlesPanier++; // Augmenter le nombre d'articles lorsque un article est ajouté au panier
        // Stocker le nombre d'articles dans le panier dans le stockage local du navigateur
        localStorage.setItem('nombreArticlesPanier', nombreArticlesPanier);
        mettreAJourCompteurPanier(nombreArticlesPanier); // Mettre à jour le compteur du panier
    };

    // Fonction pour supprimer un article du panier
    const supprimerDuPanier = () => {
        // Vérifier si le nombre d'articles est déjà à zéro pour éviter les valeurs négatives
        if (nombreArticlesPanier > 0) {
            nombreArticlesPanier--; // Réduire le nombre d'articles lorsque un article est supprimé du panier
            // Mettre à jour le stockage local avec le nouveau nombre d'articles
            localStorage.setItem('nombreArticlesPanier', nombreArticlesPanier);
            mettreAJourCompteurPanier(nombreArticlesPanier); // Mettre à jour le compteur du panier
        }
    };

    // Exemple d'utilisation : Appeler ajouterAuPanier() en réponse à un événement, comme un clic sur un bouton "Ajouter au Panier"
    // Ici, nous écoutons les clics sur un bouton hypothétique avec la classe ".btn-ajouter-au-panier"
    // Vous devez remplacer ".btn-ajouter-au-panier" par la classe réelle de vos boutons "Ajouter au Panier"
    const boutonsAjouterAuPanier = document.querySelectorAll('.btn-ajouter-au-panier');
    boutonsAjouterAuPanier.forEach(bouton => {
        bouton.addEventListener('click', ajouterAuPanier);
    });

    // Exemple d'utilisation : Appeler supprimerDuPanier() en réponse à un événement, comme un clic sur un bouton "Supprimer du Panier"
    // Ici, nous écoutons les clics sur un bouton hypothétique avec la classe ".btn-supprimer-du-panier"
    // Vous devez remplacer ".btn-supprimer-du-panier" par la classe réelle de vos boutons "Supprimer du Panier"
    const boutonsSupprimerDuPanier = document.querySelectorAll('.btn-supprimer-du-panier');
    boutonsSupprimerDuPanier.forEach(bouton => {
        bouton.addEventListener('click', supprimerDuPanier);
    });

    // Mettre à jour le compteur du panier lors du chargement de la page
    mettreAJourCompteurPanier(nombreArticlesPanier);
});
