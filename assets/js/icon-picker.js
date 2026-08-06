document.addEventListener("DOMContentLoaded", async function () {
    const input = document.querySelector("#id_icon_class");
    if (!input) return;

    // UI элементы
    const btn = document.createElement("button");
    btn.type = "button";
    btn.innerText = "🎨 Выбрать";
    btn.className = "icon-picker-btn";

    const preview = document.createElement("i");
    preview.className = input.value || "fas fa-link";
    preview.style.marginLeft = "10px";

    input.after(btn);
    btn.after(preview);

    // загрузка иконок 🔥
    let ICONS = [];

    async function loadIcons() {
        const res = await fetch("/static/js/fa-icons.json");
        ICONS = await res.json();
        renderIcons();
    }

    // модалка
    const modal = document.createElement("div");
    modal.className = "icon-modal";

    modal.innerHTML = `
        <div class="icon-modal-content">
            <h3>Выберите иконку</h3>

            <input type="text" class="icon-search" placeholder="🔍 Поиск...">

            <div class="icon-tabs">
                <button data-cat="all" class="active">Все</button>
                <button data-cat="brands">Brands</button>
                <button data-cat="solid">Solid</button>
            </div>

            <div class="icon-grid"></div>
        </div>
    `;

    document.body.appendChild(modal);

    const grid = modal.querySelector(".icon-grid");
    const search = modal.querySelector(".icon-search");
    const tabs = modal.querySelectorAll(".icon-tabs button");

    let currentCategory = "all";

    function renderIcons(filter = "") {
        grid.innerHTML = "";

        const filtered = ICONS.filter(icon => {
            const matchSearch = icon.name.includes(filter.toLowerCase());
            const matchCategory = currentCategory === "all" || icon.category === currentCategory;
            return matchSearch && matchCategory;
        });

        filtered.slice(0, 200).forEach(icon => { // ⚡ ограничение для скорости
            const el = document.createElement("i");
            el.className = icon.class;
            el.title = icon.name;

            el.onclick = () => {
                input.value = icon.class;
                preview.className = icon.class;
                modal.style.display = "none";
            };

            grid.appendChild(el);
        });
    }

    // поиск
    search.addEventListener("input", e => {
        renderIcons(e.target.value);
    });

    // вкладки
    tabs.forEach(tab => {
        tab.onclick = () => {
            tabs.forEach(t => t.classList.remove("active"));
            tab.classList.add("active");
            currentCategory = tab.dataset.cat;
            renderIcons(search.value);
        };
    });

    btn.onclick = () => {
        modal.style.display = "flex";
        search.value = "";
        renderIcons();
        search.focus();
    };

    modal.onclick = (e) => {
        if (e.target === modal) modal.style.display = "none";
    };

    loadIcons(); // 🚀 старт
});