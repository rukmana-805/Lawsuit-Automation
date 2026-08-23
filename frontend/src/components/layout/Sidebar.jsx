import { NavLink } from "react-router-dom";

import {
    LayoutDashboard,
    FileSpreadsheet,
    FileText
} from "lucide-react";

const menu = [
    {
        title: "Dashboard",
        icon: LayoutDashboard,
        path: "/"
    },
    {
        title: "CSV Download & Cleaning",
        icon: FileSpreadsheet,
        path: "/csv"
    },
    {
        title: "PDF Download",
        icon: FileText,
        path: "/pdf"
    }
];

export default function Sidebar() {

    return (

        <aside className="w-72 bg-slate-900 text-white h-screen">

            <div className="h-16 flex items-center justify-center border-b border-slate-700">

                <h2 className="text-xl font-bold">
                    Automation
                </h2>

            </div>

            <div className="mt-6 px-3">

                {menu.map((item) => {

                    const Icon = item.icon;

                    return (

                        <NavLink
                            key={item.title}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center gap-4 p-4 rounded-xl mb-2 transition
                                ${
                                    isActive
                                        ? "bg-blue-600"
                                        : "hover:bg-slate-800"
                                }`
                            }
                        >

                            <Icon size={20} />

                            {item.title}

                        </NavLink>

                    );

                })}

            </div>

        </aside>

    );

}