export default function Navbar() {
  return (
    <header className="h-16 bg-white shadow flex items-center justify-between px-8">

      <div>

        <h1 className="text-2xl font-bold text-slate-800">
          Claim Automation
        </h1>

        <p className="text-sm text-gray-500">
          CSV • PDF • AI Extraction
        </p>

      </div>

      <div className="flex gap-3">

        <button className="border border-blue-600 text-blue-600 px-5 py-2 rounded-lg hover:bg-blue-50 transition">

          Login

        </button>

        <button className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition">

          Sign Up

        </button>

      </div>

    </header>
  );
}