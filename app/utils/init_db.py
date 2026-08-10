import os
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.connection import engine, Base, SessionLocal
from app.models.brand import Brand
from app.models.category import Category
from app.models.mapping import SizeMapping
from app.models.size_chart import BrandSizeChart

def init_db():
    print("Creating tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
    
    db = SessionLocal()
    try:
        print("Clearing existing demo data...")
        db.execute(text("TRUNCATE TABLE brand_size_charts RESTART IDENTITY CASCADE"))
        db.execute(text("TRUNCATE TABLE size_mappings RESTART IDENTITY CASCADE"))
        db.execute(text("TRUNCATE TABLE brands RESTART IDENTITY CASCADE"))
        db.execute(text("TRUNCATE TABLE categories RESTART IDENTITY CASCADE"))
        db.commit()

        # 1. Insert Categories
        categories = [
            {"id": "mens_shirt", "name": "Men's Shirt"},
            {"id": "womens_shirt", "name": "Women's Shirt"},
            {"id": "mens_jeans", "name": "Men's Jeans"},
            {"id": "womens_jeans", "name": "Women's Jeans"},
            {"id": "womens_dress", "name": "Women's Dress"},
            {"id": "mens_shoes", "name": "Men's Shoes"},
            {"id": "womens_shoes", "name": "Women's Shoes"}
        ]
        for cat in categories:
            db.add(Category(id=cat["id"], name=cat["name"]))
        
        # 2. Insert Brands
        brand_names = [
            "Zara", "Zudio", "H&M", "Levi's", "Uniqlo", 
            "Nike", "Adidas", "Puma", "Gap", "Calvin Klein", 
            "Ralph Lauren", "Gucci", "Prada"
        ]
        for b_name in brand_names:
            db.add(Brand(name=b_name))
        db.commit()
        print("Brands and Categories added.")

        brands = {b.name: b for b in db.query(Brand).all()}

        # 3. Massive Mapping Generator
        # Base standard sizes
        standard_sizes = ["XS", "S", "M", "L", "XL", "XXL"]
        # Brand profiles offset (0 = True to Size, -1 = Runs Small, 1 = Runs Large)
        profiles = {
            "Zara": -1, "Zudio": -1, "H&M": 0, "Levi's": 0, "Uniqlo": 0,
            "Nike": -1, "Adidas": 0, "Puma": 0, "Gap": 1, "Calvin Klein": 0,
            "Ralph Lauren": 0, "Gucci": 1, "Prada": -1
        }
        
        mappings = []
        # Generate cross-brand mappings for shirt categories
        shirt_cats = ["mens_shirt", "womens_shirt"]
        for cat in shirt_cats:
            for src_name, src_brand in brands.items():
                for tgt_name, tgt_brand in brands.items():
                    if src_name == tgt_name: continue
                    
                    src_offset = profiles.get(src_name, 0)
                    tgt_offset = profiles.get(tgt_name, 0)
                    diff = src_offset - tgt_offset
                    
                    for i, size in enumerate(standard_sizes):
                        target_idx = i + diff
                        target_idx = max(0, min(len(standard_sizes)-1, target_idx))
                        
                        reason = "Sizing based on AI predictive model for brand variance."
                        if diff < 0: reason = f"{tgt_name} generally fits larger than {src_name}."
                        elif diff > 0: reason = f"{tgt_name} generally fits smaller than {src_name}."
                        
                        mappings.append(SizeMapping(
                            source_brand_id=src_brand.id,
                            source_size=size,
                            target_brand_id=tgt_brand.id,
                            target_size=standard_sizes[target_idx],
                            category_id=cat,
                            confidence_score=85 + (10 if diff == 0 else 0),
                            reason=reason
                        ))

        # Bulk insert mappings
        db.add_all(mappings)
        db.commit()
        print(f"Successfully auto-generated and populated {len(mappings)} size mappings!")

        # 4. Populate Brand Size Charts (for Measurement-based recommendations)
        charts = []
        for name, brand in brands.items():
            offset = profiles.get(name, 0)
            # Men's Shirt chart (Chest)
            # Standard M is ~38-40 inches. If brand runs small (offset -1), M is 36-38.
            base_chest_mins = {"XS": 32, "S": 35, "M": 38, "L": 41, "XL": 44, "XXL": 47}
            for size, c_min in base_chest_mins.items():
                shifted_min = c_min - (offset * 2) # Adjust inches based on brand profile
                charts.append(BrandSizeChart(
                    brand_id=brand.id,
                    category_id="mens_shirt",
                    target_size=size,
                    chest_min=shifted_min,
                    chest_max=shifted_min + 2
                ))
            
            # Women's Shirt chart (Chest/Waist)
            base_wchest_mins = {"XS": 30, "S": 32, "M": 34, "L": 37, "XL": 40, "XXL": 43}
            for size, c_min in base_wchest_mins.items():
                shifted_min = c_min - (offset * 1.5)
                charts.append(BrandSizeChart(
                    brand_id=brand.id,
                    category_id="womens_shirt",
                    target_size=size,
                    chest_min=int(shifted_min),
                    chest_max=int(shifted_min + 2)
                ))

            # Men's Jeans (Waist) - usually straightforward but let's add them
            waists = [28, 30, 32, 34, 36, 38, 40]
            for w in waists:
                charts.append(BrandSizeChart(
                    brand_id=brand.id,
                    category_id="mens_jeans",
                    target_size=str(w),
                    waist_min=w,
                    waist_max=w
                ))

        db.add_all(charts)
        db.commit()
        print(f"Successfully populated {len(charts)} size chart measurement rules!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
