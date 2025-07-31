export default function Footer() {
  return (
    <footer className="bg-gray-100 py-4 border-t mt-12">
      <div className="container mx-auto text-center text-gray-500 text-sm">
        © {new Date().getFullYear()} Think41. All rights reserved.
      </div>
    </footer>
  );
}
