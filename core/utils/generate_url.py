from django.utils.text import slugify
import transliterate
import re

# генерация урл
class URLGenerator:
        
    @staticmethod
    def generate_slug(text):
        try:
            base_slug = transliterate.slugify(text)
        except:
            base_slug = slugify(text, allow_unicode=False)
        
        # Убираем спецсимволы, оставляем только буквы, цифры и дефисы
        base_slug = re.sub(r'[^\w\s-]', '', base_slug).strip().lower()
        base_slug = re.sub(r'[-\s]+', '-', base_slug)

        if not base_slug:
            import uuid
            base_slug = str(uuid.uuid4())[:8]
        
        return base_slug
    
    @staticmethod
    def make_unique_slug(model, slug, instance=None, **filters):
        filter_kwargs = {'url': slug}
        filter_kwargs.update(filters)
        
        # Проверяем существующие записи
        existing = model.objects.filter(**filter_kwargs)
        if instance and instance.pk:
            existing = existing.exclude(pk=instance.pk)
        
        if not existing.exists():
            return slug
        
        # Ищем уникальный slug
        unique_slug = slug
        counter = 1
        
        while True:
            new_slug = f"{slug}-{counter}"
            filter_kwargs['url'] = new_slug
            
            existing = model.objects.filter(**filter_kwargs)
            if instance and instance.pk:
                existing = existing.exclude(pk=instance.pk)
            
            if not existing.exists():
                return new_slug
            
            counter += 1
            
            # чтобы бесконечный цикл нам ничего не сломал, остановим его
            if counter > 100:
                import uuid
                return f"{slug}-{uuid.uuid4().hex[:8]}"