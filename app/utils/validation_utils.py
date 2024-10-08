from math import ceil

def paginate(data, page, limit):
    total_members = len(data)
    total_pages = ceil(total_members / limit)
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "total_pages": total_pages,
        "total_members": total_members,
        "members": data[start:end]
    }
