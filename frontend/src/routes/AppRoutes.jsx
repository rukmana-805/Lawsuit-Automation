import { BrowserRouter, Routes, Route } from "react-router-dom";

import DashboardLayout from "../components/layout/DashboardLayout";

import Dashboard from "../pages/Dashboard";
import CsvAutomation from "../pages/CsvAutomation";
import PdfDownload from "../pages/PdfDownload";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/csv" element={<CsvAutomation />} />
          <Route path="/pdf" element={<PdfDownload />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}