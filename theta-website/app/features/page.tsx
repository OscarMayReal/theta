import Image from "next/image";
import {Header} from "@/components/header";
import { Button } from "@/components/ui/button";
import { ArrowDownToLineIcon, InfoIcon } from "lucide-react";

export default function Home() {
  return (
    <div>
      <FeaturesIntro />
      <ManageDevicesSection />
      <MinimalSoftwareSection />
      <NetSpaceSection />
    </div>
  );
}

function FeaturesIntro() {
    return (
        <div className="page-intro-section" style={{
          height: "100px"
        }}>
            <div className="page-intro-section-inner">
                <div className="page-intro-subtitle-upper">Explore Features</div>
                <div className="page-intro-title">Explore Quntem ThetaOS Features</div>
                <div className="page-intro-subtitle-lower">Discover the features that make Quntem ThetaOS the best choice for your device</div>
            </div>
        </div>
    )
}

function ManageDevicesSection() {
    return (
        <div className="page-info-section">
            <div className="page-info-section-inner">
                <div className="page-info-section-content">
                  <div className="page-info-section-subtitle">Quntem Grid</div>
                  <div className="page-info-section-title">Manage Devices</div>
                  <div className="page-info-section-text">Manage your devices from one place using Quntem Grid. Deploy software, run commands, and more.</div>
                </div>
                <div className="page-info-section-image" style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "flex-end"
                }}>
                  {/* <Button variant="outline"><ArrowDownToLineIcon /> Download</Button> */}
                </div>
            </div>
        </div>
    )
}

function MinimalSoftwareSection() {
    return (
        <div className="page-info-section">
            <div className="page-info-section-inner">
                <div className="page-info-section-content">
                  <div className="page-info-section-subtitle">Minimal Software</div>
                  <div className="page-info-section-title">Lightweight, but powerful</div>
                  <div className="page-info-section-text">Quntem ThetaOS has minimal software installed by default, giving you a lightweight experience while still being powerful enough for your needs.</div>
                </div>
                <div className="page-info-section-image" style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "flex-end"
                }}>
                  {/* <Button variant="outline"><ArrowDownToLineIcon /> Download</Button> */}
                </div>
            </div>
        </div>
    )
}

function NetSpaceSection() {
    return (
        <div className="page-info-section">
            <div className="page-info-section-inner">
                <div className="page-info-section-content">
                  <div className="page-info-section-subtitle">New: NetSpace</div>
                  <div className="page-info-section-title">Simple local file sharing</div>
                  <div className="page-info-section-text">NetSpace is a new feature that provides a simple way to share files between devices on the same network.</div>
                </div>
                <div className="page-info-section-image" style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "flex-end"
                }}>
                  {/* <Button variant="outline"><ArrowDownToLineIcon /> Download</Button> */}
                </div>
            </div>
        </div>
    )
}