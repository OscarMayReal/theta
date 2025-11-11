import gtk from "@girs/node-gtk-4.0";
import adw from "@girs/node-adw-1";
import glib from "@girs/node-glib-2.0";
import Gdk from "@girs/node-gdk-4.0";

function ManagedInfoContainer() {
    const box = new gtk.Box({
        orientation: gtk.Orientation.HORIZONTAL,
        spacing: 6,
    });
    box.setHalign(gtk.Align.CENTER);
    box.setCssClasses(["managed-info"]);
    box.append(new gtk.Label({
        label: "This device is managed by [company name]",
    }));
    return box;
}

gtk.init();
const app = new gtk.Application({
    application_id: "com.theta.login",
});
app.connect("activate", () => {
    const loginContainer = new gtk.Window({
        application: app,
        title: "Login",
        fullscreened: true,
    });
    const box = new gtk.Box({
        orientation: gtk.Orientation.VERTICAL,
        spacing: 6,
    });
    box.append(ManagedInfoContainer());
    loginContainer.setChild(box)
    loginContainer.present();
});
app.run([]);
