"use client"

import { usePathname } from "next/navigation"

export function Navigation() {
    return (
        <div className="navigation">
            <NavigationItem location="/" label="Home" />
            <NavigationItem location="/features" label="Features" />
            <NavigationItem location="/business" label="Business" />
        </div>
    )
}

export function NavigationItem({location, label}: {location: string, label: string}) {
    const path = usePathname()
    return (
        <a href={location}>
            {path == location ? <div className="navigation-item navigation-item-selected">{label}</div> : <div className="navigation-item">{label}</div>}
        </a>
    )
}