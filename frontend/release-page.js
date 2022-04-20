import ReleaseStats from "./Stats/ReleaseStats.svelte";

const registeredApps = [];
const releaseElements = document.querySelectorAll("div.release-card");

releaseElements.forEach(el => {
    let app = new ReleaseStats({
        target: el.querySelector("div.release-stats"),
        props: {
            releaseName: el.dataset.argusReleaseName,
            showTestMap: false
        }
    });
    registeredApps.push(app);
});
