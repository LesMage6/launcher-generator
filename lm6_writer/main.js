const { app, BrowserWindow, Menu, dialog, session, shell } = require("electron");
const path = require("path");

let win = null;

function createWindow() {
  win = new BrowserWindow({
    width: 1280,
    height: 860,
    minWidth: 900,
    minHeight: 600,
    backgroundColor: "#f3f4f6",
    title: "Éditeur LM6 — V4 Assistant 🇫🇷🇪🇺",
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      spellcheck: false
    }
  });
  win.loadFile(path.join(__dirname, "index.html"));
}

/* Sauvegardes natives : le bouton 💾 de l'éditeur déclenche un
   téléchargement → on le transforme en boîte de dialogue "Enregistrer sous". */
function setupDownloads() {
  session.defaultSession.on("will-download", (event, item) => {
    const defaultPath = path.join(app.getPath("documents"), item.getFilename());
    const target = dialog.showSaveDialogSync(win, {
      title: "Enregistrer le document",
      defaultPath: defaultPath,
      filters: [
        { name: "Document LM6", extensions: ["lm6doc"] },
        { name: "Page web", extensions: ["html"] },
        { name: "Markdown", extensions: ["md"] },
        { name: "Texte", extensions: ["txt"] },
        { name: "Tous les fichiers", extensions: ["*"] }
      ]
    });
    if (!target) { event.preventDefault(); return; }
    item.setSavePath(target);
  });
}

/* Le menu natif pilote les boutons existants de l'éditeur :
   zéro modification du HTML, tout reste en français. */
function buildMenu() {
  const click = (id) => () => win.webContents.executeJavaScript(
    `document.getElementById("${id}") && document.getElementById("${id}").click();`
  );

  const template = [
    {
      label: "Fichier",
      submenu: [
        { label: "Nouveau document", accelerator: "CmdOrCtrl+N", click: click("btnNewDoc") },
        { label: "Ouvrir… (.lm6doc, .md, .txt)", accelerator: "CmdOrCtrl+O", click: click("btnOpen") },
        { type: "separator" },
        { label: "Enregistrer", accelerator: "CmdOrCtrl+S", click: click("btnSave") },
        { label: "Exporter… (HTML, MD, TXT)", accelerator: "CmdOrCtrl+Shift+E", click: click("btnExport") },
        { label: "Imprimer / PDF", accelerator: "CmdOrCtrl+P", click: click("btnPrint") },
        { type: "separator" },
        { role: "quit", label: "Quitter" }
      ]
    },
    {
      label: "Édition",
      submenu: [
        { role: "undo", label: "Annuler" },
        { role: "redo", label: "Rétablir" },
        { type: "separator" },
        { role: "cut", label: "Couper" },
        { role: "copy", label: "Copier" },
        { role: "paste", label: "Coller" },
        { role: "selectAll", label: "Tout sélectionner" },
        { type: "separator" },
        { label: "Rechercher & remplacer", accelerator: "CmdOrCtrl+F", click: click("btnFind") }
      ]
    },
    {
      label: "Affichage",
      submenu: [
        { label: "Zoom +", accelerator: "CmdOrCtrl+=", click: click("zoomIn") },
        { label: "Zoom −", accelerator: "CmdOrCtrl+-", click: click("zoomOut") },
        { type: "separator" },
        { label: "Mode sombre / clair", accelerator: "CmdOrCtrl+D", click: click("btnTheme") },
        { label: "Mode focus (zen)", accelerator: "CmdOrCtrl+G", click: click("btnZen") },
        { type: "separator" },
        { role: "reload", label: "Recharger" },
        { role: "togglefullscreen", label: "Plein écran" },
        { role: "toggleDevTools", label: "Outils de développement" }
      ]
    },
    {
      label: "Outils",
      submenu: [
        { label: "Plan du document", click: click("btnOutline") },
        { label: "Statistiques & Pomodoro", click: click("btnStats") },
        { label: "Émotes & emojis", accelerator: "CmdOrCtrl+E", click: click("btnEmotes") },
        { label: "Modèles", click: click("btnTemplates") },
        { label: "Bibliothèque", click: click("btnLib") },
        { label: "Historique de versions", click: click("btnVersions") },
        { type: "separator" },
        { label: "Correction (LanguageTool 🇩🇪🇪🇺)", click: click("btnCheck") },
        { label: "Assistant IA (Mistral 🇫🇷🇪🇺)", click: click("btnAI") },
        { type: "separator" },
        { label: "Raccourcis clavier", click: click("btnHelp") }
      ]
    },
    {
      label: "Aide",
      submenu: [
        {
          label: "À propos",
          click: () => dialog.showMessageBox(win, {
            type: "info",
            title: "À propos",
            message: "Éditeur LM6 — V4 Assistant",
            detail: "Éditeur 100 % local 🇫🇷🇪🇺\nCorrection : LanguageTool (Allemagne 🇩🇪)\nIA : Mistral (France 🇫🇷, optionnelle)\nVersion native Electron pour Windows."
          })
        }
      ]
    }
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

/* Les liens http(s) du document s'ouvrent dans le navigateur, pas dans l'app. */
function setupExternalLinks() {
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//.test(url)) shell.openExternal(url);
    return { action: "deny" };
  });
}

app.whenReady().then(() => {
  setupDownloads();
  createWindow();
  buildMenu();
  setupExternalLinks();
  app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
});

app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });