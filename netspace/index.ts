import express from "express";
import fs from "fs";
import path from "path";
import os from "os";
import fileUpload from "express-fileupload";

const app = express();
const port = 1526;
const space = "netspace"
let exposedShares: ExposedShare[] = [];

app.use(fileUpload({
    useTempFiles : true,
    tempFileDir : '/tmp/'
}));

type ExposedShare = {
    name: string;
    slug: string;
    path: string;
};

// const config = {
//     exposedShares: ExposedShare[] = [
//         {   
//             name: "Shared folder 1",
//             slug: "sharedf1",
//             path: "./sharedf1",
//         }
//     ]
// };

if (fs.existsSync("./config.json")) {
    const config = JSON.parse(fs.readFileSync("./config.json", "utf-8"));
    exposedShares = config.exposedShares;
} else {
    fs.writeFileSync("./config.json", JSON.stringify({
        exposedShares: [],
    }));
    console.log("Created config.json, edit it to add your shares. read the README.md for more information");
    process.exit(0);
}

function formatExposedShare(share: ExposedShare) {
    return {
        name: share.name,
        slug: share.slug,
    };
}

function createExposedSharesData() {
    for (let share of exposedShares) {
        const data = {
            name: share.name,
            slug: share.slug,
            checkedOutFiles : [],
        }
        fs.writeFileSync(path.join(share.path, ".netspace_share.json"), JSON.stringify(data));
    }
}

function DiscoverNetwork() {
    const startIP = "192.168.1."
    const foundDevices: string[] = [];
    for (let i = 1; i <= 254; i++) {
        const ip = startIP + i;
        fetch(`http://${ip}:${port}/info`)
            .then((res) => res.json())
            .then((data) => {
                if (data.isNetSpace) {
                    console.log(`Found Netspace at ${ip}`);
                    foundDevices.push(ip);
                }
            })
            .catch((err) => {
                console.log(`Failed to connect to ${ip}`);
            });
    }
    return foundDevices;
}

app.get("/info", (req, res) => {
    const info = {
        isNetSpace: true,
        netspace: {
            space,
            version: "1.0.0",
            capabilities: {
                fileShare: {
                    status: "enabled",
                }
            }
        },
        hostname: os.hostname(),
        network: {
            foundOn: req.url.split(":")[0].split("/")[2],
        }
    };
    res.json(info);
});

app.get("/cap/fileshare", (req, res) => {
    const fileshare = {
        status: "enabled",
        exposedShares: exposedShares.map(formatExposedShare),
    };
    res.json(fileshare);
});

app.get("/cap/fileshare/share/:shareSlug/files", (req, res) => {
    const location = req.query.location || "";
    const shareSlug = req.params.shareSlug;
    const share = exposedShares.find((share) => share.slug === shareSlug);
    if (!share) {
        res.status(404).json({ error: "Share not found" });
        return;
    }
    const files = fs.readdirSync(share.path + "/" + location);
    const formattedFiles = files.map((file) => {
        return {
            name: file,
            path: path.join(share.path + "/" + location, file),
            isDir: fs.lstatSync(path.join(share.path + "/" + location, file)).isDirectory(),
        };
    });
    res.json({
        files: formattedFiles,
    });
});

app.post("/cap/fileshare/share/:shareSlug/upload", (req, res) => {
    const shareSlug = req.params.shareSlug;
    const share = exposedShares.find((share) => share.slug === shareSlug);
    if (!share) {
        res.status(404).json({ error: "Share not found" });
        return;
    }
    const file = req.files.file;
    const location = req.query.location || "";
    const filePath = path.join(share.path + "/" + location, file.name);
    file.mv(filePath);
    res.json({
        message: "File uploaded successfully",
    });
});

app.get("/cap/fileshare/share/:shareSlug/download", (req, res) => {
    const shareSlug = req.params.shareSlug;
    const share = exposedShares.find((share) => share.slug === shareSlug);
    if (!share) {
        res.status(404).json({ error: "Share not found" });
        return;
    }
    const file = req.query.file as string;
    const filePath = path.join(share.path, file);
    res.download(filePath);
});

app.listen(port, () => {
    console.log(`Netspace listening on port ${port}`);
    // const foundDevices = DiscoverNetwork();
    // console.log(`Found ${foundDevices.length} devices`);
    createExposedSharesData();
});

let placeholderIntervalID = setInterval(() => { /* noop */ }, 50)
