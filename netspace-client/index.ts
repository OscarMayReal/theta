import gtk from "@girs/node-gtk-4.0";
import adw from "@girs/node-adw-1";
import glib from "@girs/node-glib-2.0";
import Gdk from "@girs/node-gdk-4.0";

const application = new adw.Application({
    application_id: "com.theta.netspace",
});

const pages = {
    "this-device": {
        title: "This Device",
        icon: "go-home-symbolic",
        content: HomePage,
    },
    "network": {
        title: "Network",
        icon: "network-server-symbolic",
        content: NetworkPage,
    },
};

function ContentToolbar() {
    const title = new adw.WindowTitle({
        title: "NetSpace Client",
    });
    const headerBar = new adw.HeaderBar({
        title_widget: title,
    });
    return {
        headerBar,
        title,
    };
}

function HomePage() {
    const box = new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
    });
    return {
        content: box,
    }
}

function NetworkPage() {
    const box = new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
    });
    return {
        content: box,
    }
}

function navigationItem({
    icon,
    label,
    page,
}: {
    icon: string;
    label: string;
    page: string;
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
    var listitem = new gtk.ListBoxRow({
        child: box,
    });
    listitem.setName("pageitem_" + page);
    return listitem;
}

function NavigationSidebar({
    onSetPage,
}: {
    onSetPage: (page: string) => void;
}) {
    var currentPage = "this-device";
    var list = new gtk.ListBox({
        
    });
    list.setCssClasses(["navigation-sidebar"]);
    for (const [key, value] of Object.entries(pages)) {
        list.append(navigationItem({
            icon: value.icon,
            label: value.title,
            page: key,
        }));
    }
    list.connect("row-selected", (item) => {
        onSetPage(item.getName().replace("pageitem_", ""));
    });
    function setPage(page: string) {
        list.selectRow(list.getRowAtIndex(Object.keys(pages).indexOf(page)));
    }
    return {
        list,
        setPage,

    };
}

function NavigationSplitView() {
    const { headerBar, title } = ContentToolbar();
    const { list, setPage } = NavigationSidebar({
        onSetPage: (page) => {
            if (contentToolbarView == null) return;
            contentToolbarView.setContent(pages[page].content().content);
            title.setTitle(pages[page].title);
        },
    });
    var contentToolbarView = new adw.ToolbarView({
        content: pages["this-device"].content().content,
    });
    contentToolbarView.addTopBar(headerBar);
    setPage("this-device");
    return new adw.NavigationSplitView({
        sidebar: new adw.NavigationPage({
            child: list,
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