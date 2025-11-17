import Image from "next/image";
import {Header} from "@/components/header";
import { Button } from "@/components/ui/button";
import { ArrowDownToLineIcon, BuildingIcon, CompassIcon, InfoIcon, SquareArrowOutUpRightIcon } from "lucide-react";

export default function Home() {
  return (
    <div>
      <HomePageIntro />
      <GridHighlight />
    </div>
  );
}


function HomePageIntro() {
    return (
        <div className="page-intro-section">
            <div className="page-intro-section-inner">
                <div className="page-intro-subtitle-upper">Quntem ThetaOS</div>
                <div className="page-intro-title">Lightning-fast, secure, and easy to use</div>
                <div className="page-intro-subtitle-lower">Give new life to old devices, or empower your modern devices</div>
                <div className="page-intro-button-row">
                  <a href="/download"><Button variant="outline"><ArrowDownToLineIcon />Download</Button></a>
                  <a href="/features"><Button variant="outline"><InfoIcon /> Learn More</Button></a>
                </div>
            </div>
        </div>
    )
}

function GridHighlight() {
    return (
        <div className="page-info-section">
            <div className="page-info-section-inner">
                <div className="page-info-section-content">
                  <div className="page-info-section-subtitle">ThetaOS Business + Quntem Grid</div>
                  <div className="page-info-section-title">Manage everything from one place</div>
                  <div className="page-info-section-text">Quntem Grid gives you the power to manage all your ThetaOS devices from one place</div>
                </div>
                <div className="page-info-section-image" style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "flex-end"
                }}>
                  <a href="/business"><Button variant="outline"><BuildingIcon /> Explore Business</Button></a>
                </div>
            </div>
        </div>
    )
}