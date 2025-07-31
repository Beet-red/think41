import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function ProductDetailPage() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/api/products/${id}`)
      .then(res => {
        if (!res.ok) throw new Error('Product not found');
        return res.json();
      })
      .then(data => {
        setProduct(data);
        setLoading(false);
      })
      .catch(() => {
        setProduct(null);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <div className="text-center py-10">Loading...</div>;
  if (!product) return <div className="text-center py-10 text-red-600">Product not found</div>;

  return (
    <div className="container mx-auto px-4 py-10 max-w-4xl">
      <Link to="/" className="block mb-6 text-indigo-600 hover:underline font-medium">
        &larr; Back to Products
      </Link>

      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* Optional: Placeholder or actual image */}
        <div className="h-64 bg-gray-200 flex items-center justify-center text-gray-400 text-6xl font-bold mb-6 rounded-md">
          {product.name[0].toUpperCase()}
        </div>

        <h1 className="text-3xl font-extrabold mb-2">{product.name}</h1>
        <p className="text-lg text-gray-700 mb-2">{product.brand}</p>
        <p className="text-2xl font-semibold text-indigo-700 mb-4">₹{product.retail_price}</p>

        <p className="text-gray-800 mb-4">
          {product.description || "No description available for this product."}
        </p>

        <ul className="text-gray-600 space-y-2 text-sm">
          <li>
            <span className="font-semibold">Category:</span> {product.category}
          </li>
          <li>
            <span className="font-semibold">Department:</span> {product.department}
          </li>
          <li>
            <span className="font-semibold">SKU:</span> {product.sku}
          </li>
        </ul>
      </div>
    </div>
  );
}
