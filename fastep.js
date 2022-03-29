const route = (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, '', event.target.href);
    load_route();
}

const load_route = async () => {
    const path = window.location.pathname;
    const base = 'routes';
    if (path == '/' || path == '') html = await fetch(base+'/index.html').then((data) => data.text());
    else html = await fetch(base+path+'.html').then((data) => data.text());
    if (html.includes('checkfor404')) html = await fetch(base+'/404.html').then((data) => data.text());

    document.getElementById('content').innerHTML = html;
}

window.onpopstate = load_route;
window.route = route;

load_route();