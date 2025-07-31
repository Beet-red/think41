import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-indigo-700 text-white py-4 shadow-md">
      <div className="container mx-auto flex items-center justify-between px-4">
        <Link to="/" className="text-2xl font-bold tracking-tight">Think41 Shop</Link>
        <nav className="space-x-4">
          <Link to="/" className="hover:underline">Products</Link>
          {/* Add more nav links here */}
          <Link to="/departments" className="text-blue-600 hover:underline ml-4">
                Browse Departments
            </Link>

        </nav>
      </div>
    </header>
  );
}
