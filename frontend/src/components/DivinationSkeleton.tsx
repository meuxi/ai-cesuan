import { Skeleton } from '@/components/ui/skeleton'

export default function DivinationSkeleton() {
  return (
    <div className="space-y-4 md:space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="flat-card">
            <div className="p-6">
              <div className="flex items-center gap-3 md:gap-4 mb-2">
                <Skeleton className="h-12 w-12 rounded-xl" />
                <Skeleton className="h-6 w-32" />
              </div>
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4 mt-2" />
            </div>
            <div className="p-6 pt-0">
              <Skeleton className="h-4 w-24" />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

