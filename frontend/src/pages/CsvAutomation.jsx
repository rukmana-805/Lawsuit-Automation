import { useState } from "react";
import axios from "axios";

export default function CsvAutomation() {

    const [csvURL, setCSVURL] = useState(
        "https://apps.fldfs.com/LSOPReports/Reports/Report.aspx"
    );

    const [fromDate, setFromDate] = useState("");

    const [toDate, setToDate] = useState("");

    const [loading, setLoading] = useState(false);


    const handleDownload = async () => {

        if (!fromDate || !toDate) {

            alert("Please select both dates.");

            return;
        }


        try {

            setLoading(true);

            console.log("Sending request to backend...");

            const response = await axios.post(

                "http://127.0.0.1:8000/download-csv",

                {
                    from_date: fromDate,
                    to_date: toDate,
                },

                {
                    responseType: "blob",
                }
            );


            console.log("CSV received from backend.");


            // Convert backend response into a browser Blob
            const blob = new Blob(
                [response.data],
                {
                    type: "text/csv",
                }
            );


            // Create temporary URL for the file
            const url = window.URL.createObjectURL(blob);


            // Create temporary download link
            const link = document.createElement("a");

            link.href = url;

            link.download = "report.csv";


            // Trigger browser download
            document.body.appendChild(link);

            link.click();


            // Cleanup
            link.remove();

            window.URL.revokeObjectURL(url);


            console.log("CSV download triggered.");

        } catch (error) {

            console.error(
                "CSV Download Error:",
                error
            );

            alert("CSV download failed.");

        } finally {

            setLoading(false);
        }
    };


    return (
        <div className="space-y-8">

            {/* Download CSV */}

            <div className="bg-white rounded-xl shadow p-8">

                <h2 className="text-2xl font-bold mb-6">
                    Download CSV
                </h2>


                <div className="grid grid-cols-2 gap-5">

                    <input
                        type="text"
                        value={csvURL}
                        readOnly
                        className="border rounded-lg p-3"
                    />

                    <div></div>


                    <input
                        type="date"
                        value={fromDate}
                        onChange={(e) =>
                            setFromDate(e.target.value)
                        }
                        className="border rounded-lg p-3"
                    />


                    <input
                        type="date"
                        value={toDate}
                        onChange={(e) =>
                            setToDate(e.target.value)
                        }
                        className="border rounded-lg p-3"
                    />

                </div>


                <button
                    onClick={handleDownload}
                    disabled={loading}
                    className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg disabled:opacity-50"
                >

                    {loading
                        ? "Downloading..."
                        : "Download CSV"
                    }

                </button>

            </div>


            {/* Cleaning */}

            <div className="bg-white rounded-xl shadow p-8">

                <h2 className="text-2xl font-bold mb-6">
                    Clean CSV
                </h2>


                <input
                    type="file"
                    className="border p-3 rounded-lg w-full"
                />


                <button
                    className="mt-6 bg-green-600 text-white px-6 py-3 rounded-lg"
                >
                    Clean CSV
                </button>

            </div>

        </div>
    );
}