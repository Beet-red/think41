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
      })
      .catch(() => {
        setDepartments([]);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center py-10">Loading departments...</div>;

  if (departments.length === 0) return <div className="text-center py-10">No departments found.</div>;

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-8 text-center">Departments</h1>
      <ul className="space-y-4 max-w-md mx-auto">
        {departments.map(dept => (
          <li key={dept.id} className="border rounded p-4 hover:shadow-lg transition">
            <Link to={`/departments/${dept.id}`} className="text-indigo-700 font-semibold">
              {dept.name} ({dept.product_count} products)
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
