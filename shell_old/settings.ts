import gtk from "@girs/node-gtk-4.0";
import adw from "@girs/node-adw-1";
import glib from "@girs/node-glib-2.0";

function SidebarItem({
    title,
    subtitle,
}: {
    title: string;
    subtitle?: string;
}) {
    const label = new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        halign: gtk.Align.START,
        valign: gtk.Align.CENTER,
    });
    const titleWidget = new gtk.Label({
        label: title,
        halign: gtk.Align.START,
    });
    titleWidget.setCssClasses(["heading"]);
    label.append(titleWidget);
    if (subtitle) {
        const subtitleWidget = new gtk.Label({
            label: subtitle,
            halign: gtk.Align.START,
        });
        subtitleWidget.setCssClasses(["caption"]);
        label.append(subtitleWidget);
    }
    return label;
}

const app = new adw.Application();
app.on("activate", () => {
    const win = new adw.ApplicationWindow({
        application: app,
        title: "Hello World",
        default_width: 200,
        default_height: 200,
    });
    // win.setCssClasses(["devel"]);
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
    const box = new gtk.ListBox({
        selection_mode: gtk.SelectionMode.NONE,
        vexpand: false,
        height_request: -1,
    });
    box.setCssClasses(["boxed-list"]);
    const switchRow = new adw.SwitchRow({
        title: "Dark Mode",
        subtitle: "Enable dark mode",
    });
    box.append(switchRow);
    const toolbarView = new adw.ToolbarView({
        content: new adw.Clamp({
            child: box,
            vexpand: false,
        }),
    });
    toolbarView.addTopBar(headerBar);
    const sidebarBox = new gtk.ListBox({
        
    });
    sidebarBox.setCssClasses(["navigation-sidebar"]);
    sidebarBox.append(SidebarItem({
        title: "Quntem Account",
        subtitle: "Manage your Quntem account",
    }));
    sidebarBox.append(SidebarItem({
        title: "Grid Management",
        subtitle: "Manage device enrollment",
    }));
    const sidebarToolbarView = new adw.ToolbarView({
        content: sidebarBox,
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
