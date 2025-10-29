export default function RecommendationList({ target, recommendations }:any) {
  return (
    <div className="mt-12">
      <h2 className="text-2xl font-bold mb-4 text-center">
        🔍 Recommended for: <span className="text-blue-600">{target}</span>
      </h2>
      <div className="flex flex-wrap justify-center gap-4">
        {recommendations.map((r:any, i:number) => (
          <div
            key={i}
            className="bg-white shadow-md rounded-lg p-3 w-48 hover:shadow-lg transition"
          >
            <img
              src={r.image}
              alt={r.title}
              className="w-full h-40 object-contain mb-2"
            />
            <h3 className="text-sm font-semibold">{r.title}</h3>
            <p className="text-gray-600 text-sm">${r.price}</p>
            <p className="text-yellow-600 text-xs">⭐ {r.rating}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
