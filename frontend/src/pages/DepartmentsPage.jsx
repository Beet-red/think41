import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function DepartmentsPage() {
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/departments')
      .then(res => res.json())
      .then(data => {
        setDepartments(data.departments || []);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center py-10">Loading...</div>;
  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6">Departments</h1>
      <ul className="space-y-4 max-w-md mx-auto">
        {departments.map(dept => (
          <li key={dept.id} className="border rounded p-4 hover:shadow-lg transition">
            <Link to={`/departments/${dept.id}`}>
              {dept.name} <span className="text-gray-500">({dept.product_count} products)</span>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
