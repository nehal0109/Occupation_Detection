import os
from icrawler.builtin import GoogleImageCrawler

def download_contextual_images(objects, queries_dict, images_per_query=4):
    base_dir = 'contextual_dataset6'
    os.makedirs(base_dir, exist_ok=True)

    for obj in objects:
        obj_dir = os.path.join(base_dir, obj)
        os.makedirs(obj_dir, exist_ok=True)

        object_queries = queries_dict.get(obj, [])
        total_images_downloaded = 0

        for query_template in object_queries:
            try:
                crawler = GoogleImageCrawler(
                    storage={'root_dir': obj_dir}
                )

                crawler.crawl(
                    keyword=query_template,
                    max_num=images_per_query,
                    file_idx_offset=total_images_downloaded,
                    min_size=(640, 480)
                )

                total_images_downloaded += images_per_query
                print(f"Downloaded images for: {query_template}")

            except Exception as e:
                print(f"Error downloading {query_template}: {e}")

        print(f"Total images downloaded for {obj}: {total_images_downloaded}")

queries_dict = {
    'desk': [
        "freelancer working at {} in home office",
        "classroom with multiple {}",
        "student studying at {} in library corner",
        "professional setting up {} in shared workspace",
        "creative professional arranging {} with natural light"
    ],
    'whiteboard': [
        "teacher explaining concept using {} in classroom",
        "students looking at {} in class",
        "project manager brainstorming on {} during meeting",
        "researcher mapping ideas on {} in academic setting",
        "consultant presenting strategy using {} in conference room"
    ],
    'dslr-camera': [
        "photographer capturing landscape with {}",
        "documentary maker using {} in field research",
        "traveler photographing scenery with {}",
        "journalist documenting event with {}",
        "wildlife photographer using {} in natural environment"
    ],
    'tripod': [
        "wildlife photographer setting up {} in forest",
        "videographer adjusting {} on location shoot",
        "landscape photographer using {} during sunrise",
        "documentary filmmaker stabilizing {} outdoors",
        "nature photographer preparing {} in mountain setting"
    ],
    'stethoscope': [
        "doctor examining patient with {}",
        "nurse conducting health check using {}",
        "medical student practicing with {}",
        "clear image of {}",
        "different angle images of {}"
    ],
    'syringe': [
        "nurse administering vaccine with {}",
        "medical professional preparing medication with {}",
        "doctor conducting routine blood test with {}",
        "healthcare worker in vaccination center near {}",
        "medical researcher using {} in laboratory"
    ],
    'wrench': [
        "mechanic repairing car engine with {}",
        "plumber fixing pipes using {}",
        "bicycle repair technician adjusting bike with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'hammer': [
        "carpenter building wooden structure with {}",
        "construction worker on building site having {}",
        "home renovation expert using {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'tire': [
        "mechanic changing {} at auto repair shop",
        "racing team preparing vehicle {}",
        "cyclist checking {} before ride",
        "truck driver inspecting {} during long haul",
        "automotive technician working with {}"
    ],
    'guitar': [
        "musician performing with {} in small venue",
        "street performer playing {} outdoors",
        "music student practicing {}",
        "songwriter composing with {} in studio",
        "band member rehearsing with {}"
    ],
    'tractor': [
        "farmer harvesting crops with {}",
        "agricultural worker plowing field with {}",
        "rural landscape with {} during harvest",
        "farm maintenance using {}",
        "agricultural contractor working with {}"
    ],
    'construction-helmet': [
        "construction worker on building site wearing {}",
        "engineer inspecting project with {}",
        "safety inspector checking workplace",
        "architect walking construction site with {}",
        "construction team meeting with {} visible"
    ],
    'shelf': [
        "librarian organizing books on {}",
        "home office with {} in background",
        "bookstore employee arranging {}",
        "library with many book {}",
        "home organization with {} in living space"
    ],
    'piano': [
        "musician practicing {} in living room",
        "music school with student playing {}",
        "concert hall with {} in background",
        "music teacher giving lesson near {}",
        "recording studio with {} set up"
    ],
    'drum': [
        "band member playing {} in rehearsal space",
        "music school student practicing {}",
        "live music venue with {} on stage",
        "street performer with {} in public space",
        "recording studio musician with {}"
    ],
    'comb': [
        "hairstylist styling client's hair with {}",
        "makeup artist preparing model backstage with {}",
        "barber working in traditional barbershop with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'razor': [
        "barber giving professional shave with {}",
        "professional grooming before important event with {}",
        "makeup artist preparing model backstage with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'handcuffs': [
        "police officer on patrol with {}",
        "law enforcement training scenario having {}",
        "security professional during arrest procedure with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'gun': [
        "police officer on duty with {}",
        "military training exercise with {}",
        "security professional during patrol with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'sewing-machine': [
        "fashion designer working with {} in studio",
        "clear image of {}",
        "different angles images of {}",
        "costume designer preparing outfit with {}",
        "indian tailor working with {}"
    ],
    'mop': [
        "janitor cleaning hallway with {}",
        "professional cleaning service worker with {}",
        "hotel housekeeping staff working with {}",
        "indian cleaner with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'broom': [
        "street cleaner maintaining urban area with {}",
        "indian cleaner at work with {}",
        "clear image of {}",
        "different angles images of {}",
        "traditional craftsman sweeping workspace with {}",
        "outdoor event cleanup crew using {}"
    ],
    'bucket': [
        "construction worker carrying {} on site",
        "cleaning professional with {} of supplies",
        "gardener collecting water with {}",
        "beach cleanup volunteer using {}",
        "farmer collecting rainwater in {} with tractor and cow"
    ],
    'swimming-goggles': [
        "professional swimmer training in pool with {}",
        "lifeguard preparing for duty with {}",
        "competitive swimmer adjusting {}",
        "diving instructor checking equipment {}",
        "open water swimmer preparing for race with {}"
    ],
    'green-dustbin': [
        "street cleaner managing city sanitation with {}",
        "waste management professional at work with {}",
        "residential area with {} on collection day",
        "park maintenance crew using {}",
        "environmental cleanup team working with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'stumps': [
        "cricket match with {} as wickets",
        "cricket training session {}",
        "professional cricket ground setup with {}",
        "cricket coaching practice with {}",
        "amateur cricket match in local park with {}",
        "clear image of {}",
        "different angles images of {}"
    ],
    'cricket-bat': [
        "professional cricketer practicing swing with {}",
        "local cricket match in progress {}",
        "cricket coaching session with {}",
        "street cricket with amateur players with {}",
        "cricket academy training with {}",
        "clear image of {}",
        "different angles images of {}"
    ]
}

objects_to_download = list(queries_dict.keys())

download_contextual_images(objects_to_download, queries_dict, images_per_query=4)
