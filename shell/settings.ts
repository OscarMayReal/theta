import gtk from "@girs/node-gtk-4.0";
import adw from "@girs/node-adw-1";

const app = new adw.Application();
app.on("activate", () => {
    const win = new adw.ApplicationWindow({
        application: app,
        title: "Hello World",
        default_width: 200,
        default_height: 200,
    });
    const headerBar = new adw.HeaderBar({
        title_widget: new adw.WindowTitle({
            title: "Hello World",
            // subtitle: "Subtitle",
        }),
    });
    const sidebarHeader = new adw.HeaderBar({
        title_widget: new adw.WindowTitle({
            title: "Sidebar",
        }),
    });
    const button = new gtk.Button({
        icon_name: "user",
    });
    button.connect("clicked", () => {
        const aboutwin = new adw.AboutWindow({
            application: app,
            title: "About Theta Settings",
            default_width: 200,
            default_height: 200,
            application_name: "Theta Settings",
            version: "1.0.0",
            release_notes: "initial release",
            website: "https://theta.quntem.co.uk",
            issue_url: "https://github.com/ThetaOS/theta/issues",
            application_icon: "theta",
        });
        aboutwin.present();
    });
    headerBar.packEnd(button);
    // const box = new gtk.Box({
    //     orientation: gtk.Orientation.VERTICAL,
    //     spacing: 6,
    // });
    // box.append(headerBar);
    // win.setContent(box);
    const toolbarView = new adw.ToolbarView({
    
    });
    toolbarView.addTopBar(headerBar);
    const sidebarToolbarView = new adw.ToolbarView({
        
    });
    sidebarToolbarView.addTopBar(sidebarHeader);
    var navigationView = new adw.NavigationSplitView({
        sidebar: new adw.NavigationPage({
            child: sidebarToolbarView,
        }),
        content: new adw.NavigationPage({
            child: toolbarView,
        }),
    });
    win.setContent(navigationView);
    win.present();
});
app.run([]);
