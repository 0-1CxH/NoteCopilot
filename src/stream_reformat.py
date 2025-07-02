class StreamReformatter:
    @staticmethod
    def prefix_exists(s, match_tag):
        if match_tag == "left":
            partial_thinks = ["<", "<t", "<th", "<thi", "<thin", "<think"]
        else:
            partial_thinks = ["<", "</", "</t", "</th", "</thi", "</thin", "</think"]
        
        for _ in partial_thinks:
            if _ in s:
                return True
        return False


    @staticmethod
    def execute(stream):
        first_chunk_not_processed = True
        last_chunk_not_processed = True
        left_think_not_processed = True
        right_think_not_processed = True
        buffer = ""

        for chunk in stream:
            if chunk is None:
                if buffer:
                    yield buffer
                last_chunk_not_processed = False
                yield "</ai-message-component-response></ai-message>"
            
            if first_chunk_not_processed:
                first_chunk_not_processed = False
                chunk = "<ai-message>" + chunk
            
            if left_think_not_processed:
                if "<think>" in chunk:
                    chunk = chunk.replace("<think>", "<ai-message-component-think>")
                    left_think_not_processed = False
                    yield chunk
                if not buffer:
                    if StreamReformatter.prefix_exists(chunk, "left"):
                        buffer += chunk
                        continue
                
                else:
                    if StreamReformatter.prefix_exists(chunk, "left"):
                        yield buffer
                        buffer = ''
                    buffer += chunk
                    if "<think>" in buffer:
                        buffer = buffer.replace("<think>", "<ai-message-component-think>")
                        left_think_not_processed = False
                        yield buffer
                        buffer = ''
                    continue
            
            if right_think_not_processed:
                if "</think>" in chunk:
                    chunk = chunk.replace("</think>", "</ai-message-component-think><ai-message-component-response>")
                    right_think_not_processed = False
                    yield chunk
                if not buffer:
                    if StreamReformatter.prefix_exists(chunk, "right"):
                        buffer += chunk
                        continue
                
                else:
                    if StreamReformatter.prefix_exists(chunk, "right"):
                        yield buffer
                        buffer = ''
                    buffer += chunk
                    if "</think>" in buffer:
                        buffer = buffer.replace("</think>", "</ai-message-component-think><ai-message-component-response>")
                        right_think_not_processed = False
                        yield buffer
                        buffer = ''
                    continue


            yield chunk
        
        if last_chunk_not_processed:
            if buffer:
                yield buffer
            yield "</ai-message-component-response></ai-message>"


if __name__ == "__main__":
    print(list(StreamReformatter.execute(
        ["ssss",  "ssss<",  "ssss<", "th", "ink", ">ppppp", "<", "ssss", "<", "</t", "hink", ">aaaaa"]
    )))