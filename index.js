window.addEventListener('load', function(){
    new Glider(document.querySelector('.glider'), {
        slidesToShow: 3, 
        slidesToScroll: 1,
        draggable: true,
        dots: '.dots',
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            },
            {
                breakpoint: 300,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }
        ]
    });
});


function toggleMenu() {
    const fundo_menu = document.querySelector('.navbar');
    const menu = document.querySelector('.nav-menu');

    fundo_menu.classList.toggle('active');
    menu.classList.toggle('active');
}

const apiUrl = 'https://app.ketzim.com/webservice/get-instagram-info/ProtegePisoDourados/?Token=Ld7gRCo9JtIRw0Ub3sC3JxuCgIMvSAzJEMLSutCPh9XosGzzqpdlhsqhUYXHHRyHKPZ6MHcwfl8Dl7ohzsKv7jpihquxHvFmEkFJ';

function displayUserProfile(profile) {
    document.getElementById('profile-picture').src = profile.profile_picture_url;
    document.getElementById('username').textContent = `@${profile.username}`;
    document.getElementById('followers').textContent = `Seguidores: ${profile.followers_count}`;
    document.getElementById('posts').textContent = `Posts: ${profile.media_count}`;
}

async function fetchInstagramData() {
    try {
        const response = await fetch(apiUrl);
        const data = await response.json();
        displayUserProfile(data.perfil);
        displayPosts(data.midias.data);
    } catch (error) {
        console.error('Erro ao buscar dados da API:', error);
    }
}

function displayPosts(posts) {
    const gridContainer = document.querySelector('.glider-custom');
    gridContainer.innerHTML = ''; 

    const limitedPosts = posts.slice(0, 50); 

    limitedPosts.forEach(post => {

        if (post.media_type === 'VIDEO') {
            return;
        }
        
        const postCard = document.createElement('div');
        postCard.classList.add('post-card-custom');

        postCard.innerHTML = `
            <a href="${post.permalink}" target="_blank"> <!-- Link clicável -->
                <img src="${post.media_url}" alt="${post.caption}">
            </a>
        `;

        gridContainer.appendChild(postCard);
    });

    new Glider(document.querySelector('.glider-custom'), {
        slidesToShow: 1, 
        slidesToScroll: 1, 
        draggable: false, 
        arrows: {
            prev: '.glider-prev-custom', 
            next: '.glider-next-custom'  
        },
        responsive: [
            {
                breakpoint: 1024, 
                settings: {
                    slidesToShow: 3, 
                    slidesToScroll: 3
                }
            },
             {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2, 
                    slidesToScroll: 2
                }
            },
            {
                breakpoint: 480, 
                settings: {
                    slidesToShow: 1, 
                    slidesToScroll: 1
                }
            }
        ]
    });
}

fetchInstagramData();

function waitForJivoChat() {
    if (typeof jivo_api !== 'undefined') {
        document.getElementById('openChatBtn').addEventListener('click', function() {
            setTimeout(function() {
                jivo_api.open();
            }, 100); 
        });
    } else {
        setTimeout(waitForJivoChat, 500);
    }
}

waitForJivoChat();

const iframeContainer = document.querySelector('.container-iframe');
const iframeUrl = 'https://app.ketzim.com/webservice/mapa/dourados/';


fetch(iframeUrl)
  .then(response => {
    if (response.ok) {
      iframeContainer.innerHTML = `
        <iframe src="${iframeUrl}" class="iframe-full" title="Mapa das obras realizadas na cidade da franquia"></iframe>
      `;
    } else {
      iframeContainer.innerHTML = '<p style="color: red" >O mapa com as obras está temporariamente indisponível. Por favor, tente novamente mais tarde.</p>';
    }
  })
  .catch(error => {
    iframeContainer.innerHTML = '<p>O mapa está temporariamente indisponível. Por favor, tente novamente mais tarde.</p>';
    console.error('Erro ao carregar o mapa:', error);
  });
