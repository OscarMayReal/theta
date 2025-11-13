import gtk from "@girs/node-gtk-4.0";
import adw from "@girs/node-adw-1";
import glib from "@girs/node-glib-2.0";
import Gdk from "@girs/node-gdk-4.0";

const application = new adw.Application({
    application_id: "com.theta.netspace",
});

function ContentToolbar() {
    return new adw.HeaderBar({
        title_widget: new adw.WindowTitle({
            title: "Netspace",
        }),
    });
}

function HomePage() {
    return new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
    });
}

function NetworkPage() {
    return new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
    });
}

function navigationItem({
    icon,
    label,
}: {
    icon: string;
    label: string;
}) {
    var box = new gtk.Box({
        orientation: gtk.Orientation.HORIZONTAL,
        spacing: 6,
    });
    box.append(new gtk.Image({
        icon_name: icon,
    }));
    box.append(new gtk.Label({
        label: label,
    }));
    return box;
}

function CreateSidebar() {
    var list = new gtk.ListBox({
        
    });
    list.setCssClasses(["navigation-sidebar"]);
    list.append(navigationItem({
        icon: "go-home-symbolic",
        label: "This Device",
    }));
    list.append(navigationItem({
        icon: "network-server-symbolic",
        label: "Network",
    }));
    return list;
}

function NavigationSplitView() {
    var contentToolbarView = new adw.ToolbarView({
        content: new gtk.Box({
            orientation: gtk.Orientation.VERTICAL,
            spacing: 6,
        }),
    });
    contentToolbarView.addTopBar(ContentToolbar());
    return new adw.NavigationSplitView({
        sidebar: new adw.NavigationPage({
            child: CreateSidebar(),
        }),
        content: new adw.NavigationPage({
            child: contentToolbarView,
        }),
    });
}

application.connect("activate", () => {
    const window = new adw.ApplicationWindow({
        application,
        title: "Netspace",
        default_width: 800,
        default_height: 600,
    });
    var splitView = NavigationSplitView();
    window.setContent(splitView);
    window.present();
});

application.run([]);