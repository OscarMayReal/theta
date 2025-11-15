import gtk from "@girs/node-gtk-4.0";

function NetworkPage() {
    const box = new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
    });
    box.append(new gtk.Label({
        label: "Network",
    }));
    return {
        content: box,
    }
}

export default {
    content: NetworkPage,
    title: "Network",
    icon: "network-server-symbolic",
}
