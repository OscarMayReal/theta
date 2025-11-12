import { Button } from "./ui/button";
import { ArrowDownToLineIcon } from "lucide-react";
import { Navigation } from "./navigation";

export function Header() {
    return (
        <header className="header">
            <div className="header-inner">
                <img src="/thetalogo.svg" alt="Logo" style={{
                    height: "25px",
                    width: "auto"
                }} />
                <div style={{flex: 1}}/>
                <Navigation />
                <Button variant={"outline"} size={"sm"}><ArrowDownToLineIcon /> Download Now</Button>
            </div>
        </header>
    )
}