# 🎨 Exemples de Personnalisation pour la Page Promo

## 🔧 Configuration Rapide

### 1. Remplacer l'ID du Bot
Remplacez `1397194777098981517` par l'ID de votre bot dans `templates/promo.html` :

```html
<!-- Recherchez cette ligne (environ ligne 71 et 214) -->
<a href="https://discord.com/api/oauth2/authorize?client_id=1397194777098981517&permissions=8&scope=bot%20applications.commands">

<!-- Remplacez par -->
<a href="https://discord.com/api/oauth2/authorize?client_id=VOTRE_BOT_ID&permissions=8&scope=bot%20applications.commands">
```

### 2. Personnaliser le Nom et la Description

```html
<!-- Changez le nom du bot -->
<h1>Summer Bot</h1>
<!-- En -->
<h1>Votre Bot</h1>

<!-- Changez la description -->
<p class="subtitle">Le Bot Discord Multi-Fonctionnel Ultime</p>
<!-- En -->
<p class="subtitle">Votre Description Personnalisée</p>
```

### 3. Modifier les Statistiques

```html
<!-- Dans la section stats -->
<div class="stat-item">
    <h3>33+</h3>
    <p>Commandes Slash</p>
</div>
<!-- Changez selon vos commandes réelles -->
```

## 🎨 Personnalisation Avancée

### Changer les Couleurs
Modifiez les gradients CSS dans le `<style>` :

```css
/* Gradient principal */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Remplacez par vos couleurs */
background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
```

### Ajouter Votre Logo
Remplacez l'icône robot par votre image :

```html
<!-- Actuel -->
<div class="bot-avatar">
    <i class="fas fa-robot"></i>
</div>

<!-- Avec votre logo -->
<div class="bot-avatar">
    <img src="URL_VERS_VOTRE_LOGO" alt="Logo" style="width: 64px; height: 64px; border-radius: 50%;">
</div>
```

### Modifier les Liens Sociaux

```html
<!-- Support Server -->
<a href="https://discord.gg/your-support-server" target="_blank">Support</a>
<!-- Remplacez par votre serveur -->

<!-- GitHub -->
<a href="https://github.com/N4ole/Discord-bot" target="_blank">GitHub</a>
<!-- Remplacez par votre repo -->
```

## 📱 Features à Ajouter

### 1. Compteur de Serveurs en Temps Réel
Ajoutez une API pour afficher le nombre de serveurs :

```javascript
// Dans le JavaScript de la page
fetch('/api/server_count')
    .then(response => response.json())
    .then(data => {
        document.querySelector('.server-count').textContent = data.servers;
    });
```

### 2. Témoignages
Ajoutez une section témoignages :

```html
<section class="testimonials">
    <div class="container">
        <h2>Ce que disent nos utilisateurs</h2>
        <div class="testimonials-grid">
            <div class="testimonial">
                <p>"Le meilleur bot de modération que j'ai utilisé !"</p>
                <span>- Admin de ServeurCool</span>
            </div>
        </div>
    </div>
</section>
```

### 3. FAQ Section
Ajoutez une FAQ :

```html
<section class="faq">
    <div class="container">
        <h2>Questions Fréquentes</h2>
        <div class="faq-item">
            <h3>Comment inviter le bot ?</h3>
            <p>Cliquez simplement sur le bouton "Inviter" et sélectionnez votre serveur !</p>
        </div>
    </div>
</section>
```

## 🔧 Intégrations Avancées

### 1. Google Analytics
Ajoutez le tracking :

```html
<!-- Dans le <head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 2. Métadonnées OpenGraph
Personnalisez les aperçus sur les réseaux sociaux :

```html
<meta property="og:title" content="Votre Bot - Description">
<meta property="og:description" content="Description de votre bot">
<meta property="og:image" content="URL_VERS_IMAGE_PREVIEW">
<meta property="og:url" content="https://votre-domaine.com/promo">
```

### 3. Rich Snippets
Ajoutez du JSON-LD pour le SEO :

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Votre Bot",
  "description": "Description de votre bot Discord",
  "applicationCategory": "CommunicationApplication",
  "operatingSystem": "Discord"
}
</script>
```

## 🚀 Optimisations Performance

### 1. Minification CSS
Minifiez le CSS pour la production.

### 2. Lazy Loading
Ajoutez le lazy loading pour les images :

```html
<img src="image.jpg" loading="lazy" alt="Description">
```

### 3. Service Worker
Ajoutez un service worker pour le cache.

## 📊 Analytics et Tracking

### Boutons d'Invitation
Trackez les clics sur les boutons d'invitation :

```javascript
document.querySelectorAll('.btn-primary').forEach(btn => {
    btn.addEventListener('click', () => {
        gtag('event', 'click', {
            'event_category': 'invitation',
            'event_label': 'promo_page'
        });
    });
});
```

### Heat Maps
Intégrez Hotjar ou Crazy Egg pour analyser le comportement des utilisateurs.

---

**Note** : Redémarrez le serveur Flask après chaque modification pour voir les changements !
