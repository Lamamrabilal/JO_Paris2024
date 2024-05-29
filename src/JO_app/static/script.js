document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const closeSidebar = document.querySelector('.close-sidebar');

    menuToggle.addEventListener('click', function() {
        menuToggle.classList.toggle('menu-open');
        sidebar.style.left = (sidebar.style.left === '-350px') ? '0' : '-350px';
    });

    closeSidebar.addEventListener('click', function() {
        menuToggle.classList.remove('menu-open');
        sidebar.style.left = '-350px';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    
    const cartCountElement = document.querySelector('.cart-count');

    
    let nombreArticlesPanier = localStorage.getItem('nombreArticlesPanier');

   
    if (!nombreArticlesPanier) {
        nombreArticlesPanier = 0;
    } else {
     
        nombreArticlesPanier = parseInt(nombreArticlesPanier);
    }


    const mettreAJourCompteurPanier = (count) => {
        if (cartCountElement) {
            cartCountElement.textContent = count;
        }
    };

    const ajouterAuPanier = () => {
    nombreArticlesPanier++; 

    localStorage.setItem('nombreArticlesPanier', nombreArticlesPanier);
    mettreAJourCompteurPanier(nombreArticlesPanier); 

 
    nombreArticlesPanier = 0;
};



    const supprimerDuPanier = () => {
        
        if (nombreArticlesPanier > 0) {
            nombreArticlesPanier--;
  
            localStorage.setItem('nombreArticlesPanier', nombreArticlesPanier);
            mettreAJourCompteurPanier(nombreArticlesPanier); 
        }
    };

  
    const boutonsAjouterAuPanier = document.querySelectorAll('.btn-ajouter-au-panier');
    boutonsAjouterAuPanier.forEach(bouton => {
        bouton.addEventListener('click', ajouterAuPanier);
    });

  
    const boutonsSupprimerDuPanier = document.querySelectorAll('.btn-supprimer-du-panier');
    boutonsSupprimerDuPanier.forEach(bouton => {
        bouton.addEventListener('click', supprimerDuPanier);
    });

    
    mettreAJourCompteurPanier(nombreArticlesPanier);
});

document.addEventListener("DOMContentLoaded", function() {
  
    const contenu = document.getElementById('contenu');
    const url = '/JO_app/home/';

    fetch(url)
        .then(response => response.text())
        .then(html => {
            
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;

            
            const nouveauContenu = tempDiv.querySelector('main').innerHTML;

            contenu.innerHTML = nouveauContenu;
        })
        .catch(error => {
            console.error('Une erreur s\'est produite : ', error);
        });
});
